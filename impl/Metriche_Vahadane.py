import numpy as np
import cv2
import pandas as pd
from sklearn.decomposition import DictionaryLearning
from scipy.stats import pearsonr
from skimage.metrics import structural_similarity as ssim

# =========================================================
# 0) Caricamento PanNuke fold 2
# =========================================================
pannuke_path = "Percorso_al_file_images.npy"
images_np = np.load(pannuke_path)

if images_np.dtype != np.uint8:
    images_np = np.clip(images_np, 0, 255).astype(np.uint8)

print("Loaded:", images_np.shape, images_np.dtype)  # (N,256,256,3)

# =========================================================
# 1) Utility: brightness standardization
# =========================================================
def standardize_brightness(I):
    I = I.astype(np.float32)
    p = np.percentile(I, 95)
    if p <= 0:
        return np.clip(I, 0, 255).astype(np.uint8)
    return np.clip(I * 255.0 / p, 0, 255).astype(np.uint8)

def rgb_to_od(I):
    I = I.astype(np.float32)
    I[I == 0] = 1.0
    return -np.log(I / 255.0)

def od_to_rgb(OD):
    return np.clip(255.0 * np.exp(-OD), 0, 255).astype(np.uint8)

def normalize_rows(A):
    n = np.linalg.norm(A, axis=1, keepdims=True)
    n[n == 0] = 1.0
    return A / n

def notwhite_mask(I, thresh=0.8):
    return np.min(I, axis=2) < (thresh * 255)

# =========================================================
# 2) Vahadane: stima stain matrix + concentrazioni
# =========================================================
def get_stain_matrix_vahadane(I, threshold=0.8, n_components=2, alpha=0.1, max_pixels=10000):
    mask = notwhite_mask(I, thresh=threshold).reshape(-1)
    OD = rgb_to_od(I).reshape((-1, 3))
    OD = OD[mask]

    if OD.shape[0] < 50:
        # fallback se quasi tutta background
        OD = rgb_to_od(I).reshape((-1, 3))

    if OD.shape[0] > max_pixels:
        idx = np.random.choice(OD.shape[0], max_pixels, replace=False)
        OD = OD[idx]

    dl = DictionaryLearning(
        n_components=n_components,
        alpha=alpha,
        max_iter=1000,
        fit_algorithm="cd",
        transform_algorithm="lasso_cd",
        positive_code=True,
        positive_dict=True,
        random_state=42
    )

    D = dl.fit(OD).components_

    # ordina per consistenza (euristica)
    if D[0, 0] < D[1, 0]:
        D = D[[1, 0], :]

    return normalize_rows(D)

def get_concentrations(I, stain_matrix):
    OD = rgb_to_od(I).reshape((-1, 3))
    C, _, _, _ = np.linalg.lstsq(stain_matrix.T, OD.T, rcond=None)
    C = C.T
    C = np.maximum(C, 0)
    return C

class VahadaneNormalizer:
    def __init__(self, threshold=0.8, alpha=0.1):
        self.threshold = threshold
        self.alpha = alpha
        self.stain_tgt = None
        self.mu_tgt = None
        self.sigma_tgt = None

    def fit(self, target_rgb):
        target_rgb = standardize_brightness(target_rgb)
        self.stain_tgt = get_stain_matrix_vahadane(
            target_rgb, threshold=self.threshold, alpha=self.alpha
        )
        C_tgt = get_concentrations(target_rgb, self.stain_tgt)
        self.mu_tgt = np.mean(C_tgt, axis=0)
        self.sigma_tgt = np.std(C_tgt, axis=0)
        self.sigma_tgt[self.sigma_tgt == 0] = 1.0

    def transform(self, src_rgb):
        if self.stain_tgt is None:
            raise RuntimeError("Call fit(target) before transform(source).")

        src_rgb = standardize_brightness(src_rgb)
        stain_src = get_stain_matrix_vahadane(
            src_rgb, threshold=self.threshold, alpha=self.alpha
        )
        C_src = get_concentrations(src_rgb, stain_src)

        mu_src = np.mean(C_src, axis=0)
        sigma_src = np.std(C_src, axis=0)
        sigma_src[sigma_src == 0] = 1.0

        C_norm = (C_src - mu_src) / sigma_src
        C_norm = C_norm * self.sigma_tgt + self.mu_tgt

        OD_norm = C_norm @ self.stain_tgt
        OD_img = OD_norm.reshape(src_rgb.shape)
        return od_to_rgb(OD_img)

# =========================================================
# 3) H/E maps con Ruifrok–Johnston (per metriche, coerente)
# =========================================================
def _rgb_to_od_rj(img_rgb, Io=255.0):
    img = img_rgb.astype(np.float32)
    img[img == 0] = 1.0
    return -np.log(img / Io)

def _get_rj_matrix():
    H = np.array([0.650, 0.704, 0.286], dtype=np.float32)
    E = np.array([0.072, 0.990, 0.105], dtype=np.float32)
    D = np.cross(H, E)
    M = np.stack([H, E, D], axis=1)
    M = M / (np.linalg.norm(M, axis=0, keepdims=True) + 1e-8)
    return M

_RJ_M = _get_rj_matrix()
_RJ_M_INV = np.linalg.inv(_RJ_M)

def he_density_maps(img_rgb):
    od = _rgb_to_od_rj(img_rgb).reshape((-1, 3))
    C = od @ _RJ_M_INV
    H_map = np.clip(C[:, 0], 0, 3).reshape(img_rgb.shape[:2]).astype(np.float32)
    E_map = np.clip(C[:, 1], 0, 3).reshape(img_rgb.shape[:2]).astype(np.float32)
    return H_map, E_map

# =========================================================
# 4) Metriche (Pearson safe)
# =========================================================
def rrmse(a, b, eps=1e-8):
    a = a.astype(np.float32).ravel()
    b = b.astype(np.float32).ravel()
    return float(np.linalg.norm(a - b) / (np.linalg.norm(b) + eps))

def safe_pearson(a, b, eps=1e-6):
    if np.std(a) < eps or np.std(b) < eps:
        return np.nan
    r, _ = pearsonr(a.ravel(), b.ravel())
    return float(r)

def qssim_like(a, b):
    a = a.astype(np.float32)
    b = b.astype(np.float32)
    dr = float(max(a.max(), b.max()) - min(a.min(), b.min()))
    if dr < 1e-6:
        dr = 1.0
    return float(ssim(a, b, data_range=dr))

def compute_metrics(norm_rgb, target_rgb):
    Hn, En = he_density_maps(norm_rgb)
    Ht, Et = he_density_maps(target_rgb)

    rH = rrmse(Hn, Ht)
    rE = rrmse(En, Et)
    pH = safe_pearson(Hn, Ht)
    pE = safe_pearson(En, Et)
    sH = qssim_like(Hn, Ht)
    sE = qssim_like(En, Et)

    return {
        "rRMSE_mean": 0.5 * (rH + rE),
        "Pearson_mean": np.nanmean([pH, pE]),
        "QSSIM_mean": 0.5 * (sH + sE),
    }
# =========================================================
# Parametri FAST (consigliati) #Usiamo questi parametri per velocizzare un pò la normalizzazione , altrimenti si rischia di impiegare diverse ore per il corretto utilizzo del codice
# =========================================================
VAH_MAX_PIXELS = 3000     # 2000–5000
VAH_MAX_ITER   = 250      # 200–400
VAH_ALPHA      = 0.1
VAH_THRESH     = 0.8

def get_stain_matrix_vahadane_fast(I, threshold=VAH_THRESH, n_components=2, alpha=VAH_ALPHA,
                                   max_pixels=VAH_MAX_PIXELS, max_iter=VAH_MAX_ITER):
    mask = notwhite_mask(I, thresh=threshold).reshape(-1)
    OD = rgb_to_od(I).reshape((-1, 3))
    OD = OD[mask]

    if OD.shape[0] < 50:
        OD = rgb_to_od(I).reshape((-1, 3))

    if OD.shape[0] > max_pixels:
        idx = np.random.choice(OD.shape[0], max_pixels, replace=False)
        OD = OD[idx]

    dl = DictionaryLearning(
        n_components=n_components,
        alpha=alpha,
        max_iter=max_iter,          # <<< ridotto
        fit_algorithm="cd",
        transform_algorithm="lasso_cd",
        positive_code=True,
        positive_dict=True,
        random_state=42
    )

    D = dl.fit(OD).components_
    if D[0, 0] < D[1, 0]:
        D = D[[1, 0], :]
    return normalize_rows(D)

class VahadaneNormalizerFast:
    def __init__(self):
        self.stain_tgt = None
        self.mu_tgt = None
        self.sigma_tgt = None

    def fit(self, target_rgb):
        target_rgb = standardize_brightness(target_rgb)
        self.stain_tgt = get_stain_matrix_vahadane_fast(target_rgb)
        C_tgt = get_concentrations(target_rgb, self.stain_tgt)
        self.mu_tgt = np.mean(C_tgt, axis=0)
        self.sigma_tgt = np.std(C_tgt, axis=0)
        self.sigma_tgt[self.sigma_tgt == 0] = 1.0

    def transform(self, src_rgb):
        src_rgb = standardize_brightness(src_rgb)
        stain_src = get_stain_matrix_vahadane_fast(src_rgb)   # <<< ancora per-source, ma più leggero
        C_src = get_concentrations(src_rgb, stain_src)

        mu_src = np.mean(C_src, axis=0)
        sigma_src = np.std(C_src, axis=0)
        sigma_src[sigma_src == 0] = 1.0

        C_norm = (C_src - mu_src) / sigma_src
        C_norm = C_norm * self.sigma_tgt + self.mu_tgt

        OD_norm = C_norm @ self.stain_tgt
        OD_img = OD_norm.reshape(src_rgb.shape)
        return od_to_rgb(OD_img)

# =========================================================
# Esperimento: TUTTO il dataset, 1 target
# =========================================================
tgt_idx = XXXX  # <<< scegli tu l'indice target (UNO SOLO)
tgt_rgb = images_np[tgt_idx]

vah = VahadaneNormalizerFast()
vah.fit(tgt_rgb)

rows = []
N_total = images_np.shape[0]

for src_idx in range(N_total):
    if src_idx % 100 == 0:
        print(f"Processing {src_idx}/{N_total}")

    src_rgb = images_np[src_idx]
    norm_rgb = vah.transform(src_rgb)
    m = compute_metrics(norm_rgb, tgt_rgb)
    rows.append(m)

df_vah = pd.DataFrame(rows)

# =========================================================
# 7) OUTPUT: mostra SOLO media e std (no singole immagini)
# =========================================================
print("\n=== Summary OVERALL (mean ± std) su tutte le sorgenti e tutti i target ===")
summary_overall = df_vah[["rRMSE_mean", "Pearson_mean", "QSSIM_mean"]].agg(["mean", "std"])
display(summary_overall)

print("\n=== Percentuale Pearson NaN (mappe costanti) ===")
print(df_vah["Pearson_mean"].isna().mean())
