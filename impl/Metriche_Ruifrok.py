import numpy as np
import pandas as pd
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
# 1) Utility: brightness standardization (consigliata)
# =========================================================
def standardize_brightness(I):
    I = I.astype(np.float32)
    p = np.percentile(I, 95)
    if p <= 0:
        return np.clip(I, 0, 255).astype(np.uint8)
    return np.clip(I * 255.0 / p, 0, 255).astype(np.uint8)

# =========================================================
# 2) Ruifrok–Johnston: OD <-> RGB + Matrice H/E (fissa)
# =========================================================
def rgb_to_od(img_rgb, Io=255.0):
    img = img_rgb.astype(np.float32)
    img[img == 0] = 1.0
    return -np.log(img / Io)

def od_to_rgb(od, Io=255.0):
    return np.clip(Io * np.exp(-od), 0, 255).astype(np.uint8)

def get_rj_matrix():
    # Vettori H ed E standard
    H = np.array([0.650, 0.704, 0.286], dtype=np.float32)
    E = np.array([0.072, 0.990, 0.105], dtype=np.float32)
    D = np.cross(H, E)
    M = np.stack([H, E, D], axis=1)  # (3,3)
    M = M / (np.linalg.norm(M, axis=0, keepdims=True) + 1e-8)
    return M

RJ_M = get_rj_matrix()
RJ_INV = np.linalg.inv(RJ_M)

def concentrations_rj(img_rgb):
    OD = rgb_to_od(img_rgb).reshape((-1, 3))
    C = OD @ RJ_INV  # (N,3) -> [H,E,D]
    return C

def reconstruct_from_conc(C, shape):
    OD = C @ RJ_M
    OD_img = OD.reshape((shape[0], shape[1], 3))
    OD_img = np.clip(OD_img, 0, 3)
    return od_to_rgb(OD_img)

def he_maps(img_rgb):
    C = concentrations_rj(img_rgb)
    H = np.clip(C[:, 0], 0, 3).reshape(img_rgb.shape[:2]).astype(np.float32)
    E = np.clip(C[:, 1], 0, 3).reshape(img_rgb.shape[:2]).astype(np.float32)
    return H, E

# =========================================================
# 3) RJ Normalizer (target-based)
# =========================================================
class RuifrokJohnstonNormalizer:
    def __init__(self):
        self.mu_tgt = None
        self.sigma_tgt = None

    def fit(self, target_rgb):
        target_rgb = standardize_brightness(target_rgb)
        C_tgt = concentrations_rj(target_rgb)

        HE = C_tgt[:, :2]
        self.mu_tgt = np.mean(HE, axis=0)
        self.sigma_tgt = np.std(HE, axis=0)
        self.sigma_tgt[self.sigma_tgt == 0] = 1.0

    def transform(self, src_rgb):
        if self.mu_tgt is None:
            raise RuntimeError("Call fit(target) before transform(source).")

        src_rgb = standardize_brightness(src_rgb)
        C_src = concentrations_rj(src_rgb)

        HE = C_src[:, :2]
        D  = C_src[:, 2:3]  # lasciamo invariato

        mu_src = np.mean(HE, axis=0)
        sigma_src = np.std(HE, axis=0)
        sigma_src[sigma_src == 0] = 1.0

        HE_norm = (HE - mu_src) / sigma_src
        HE_norm = HE_norm * self.sigma_tgt + self.mu_tgt

        C_norm = np.concatenate([HE_norm, D], axis=1)
        return reconstruct_from_conc(C_norm, src_rgb.shape)

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
    Hn, En = he_maps(norm_rgb)
    Ht, Et = he_maps(target_rgb)

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
# 5) TARGET: scegli manualmente (1 o più)
# =========================================================
tgt_indices = [XXXX]  # <-- qui si mette il numero dell'immagine target(o più)

# =========================================================
# 6) Esperimento: sorgenti = TUTTO il dataset
# =========================================================
N_total = images_np.shape[0]
rows = []

for tgt_idx in tgt_indices:
    tgt_rgb = images_np[tgt_idx]

    rj = RuifrokJohnstonNormalizer()
    rj.fit(tgt_rgb)

    for src_idx in range(N_total):
        src_rgb = images_np[src_idx]
        norm_rgb = rj.transform(src_rgb)

        m = compute_metrics(norm_rgb, tgt_rgb)
        m["tgt_idx"] = int(tgt_idx)
        rows.append(m)

df_rj = pd.DataFrame(rows)

# =========================================================
# 7) OUTPUT: SOLO media e std
# =========================================================
print("\n=== Summary OVERALL (mean ± std) su tutte le sorgenti e tutti i target ===")
summary_overall = df_rj[["rRMSE_mean", "Pearson_mean", "QSSIM_mean"]].agg(["mean", "std"])
display(summary_overall)

print("\n=== Percentuale Pearson NaN (mappe costanti) ===")
print(df_rj["Pearson_mean"].isna().mean())


