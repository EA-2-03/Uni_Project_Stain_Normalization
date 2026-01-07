import numpy as np
import cv2
import pandas as pd
from sklearn.decomposition import PCA
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

# =========================================================
# 2) MACENKO NORMALIZER
# =========================================================
def rgb_to_od(image_rgb, Io=240.0):
    image_rgb = image_rgb.astype(np.float32)
    image_rgb[image_rgb == 0] = 1
    return -np.log(image_rgb / Io)

def od_to_rgb(od, Io=240.0):
    return np.clip(Io * np.exp(-od), 0, 255).astype(np.uint8)

def get_stain_matrix_macenko(image_rgb, Io=240.0, beta=0.15, alpha=1.0):
    od = rgb_to_od(image_rgb, Io=Io).reshape((-1, 3))

    mask = np.any(od > beta, axis=1)
    od_fg = od[mask]
    if od_fg.shape[0] < 10:
        od_fg = od

    pca = PCA(n_components=2)
    od_proj = pca.fit_transform(od_fg)
    eigvecs = pca.components_.T

    phi = np.arctan2(od_proj[:, 1], od_proj[:, 0])
    min_phi = np.percentile(phi, alpha)
    max_phi = np.percentile(phi, 100 - alpha)

    v1 = eigvecs @ np.array([np.cos(min_phi), np.sin(min_phi)], dtype=np.float32)
    v2 = eigvecs @ np.array([np.cos(max_phi), np.sin(max_phi)], dtype=np.float32)

    H = v1 / (np.linalg.norm(v1) + 1e-8)
    E = v2 / (np.linalg.norm(v2) + 1e-8)
    return np.vstack([H, E])

class MacenkoNormalizer:
    def __init__(self, Io=240.0):
        self.Io = Io
        self.stain_tgt = None
        self.mu_tgt = None
        self.sigma_tgt = None

    def fit(self, target_rgb):
        target_rgb = standardize_brightness(target_rgb)
        stain = get_stain_matrix_macenko(target_rgb, Io=self.Io)
        od = rgb_to_od(target_rgb, Io=self.Io).reshape((-1, 3))

        C, _, _, _ = np.linalg.lstsq(stain.T, od.T, rcond=None)
        C = C.T

        self.stain_tgt = stain
        self.mu_tgt = np.mean(C, axis=0)
        self.sigma_tgt = np.std(C, axis=0)
        self.sigma_tgt[self.sigma_tgt == 0] = 1.0

    def transform(self, src_rgb):
        if self.stain_tgt is None:
            raise RuntimeError("Call fit(target) before transform(source).")

        src_rgb = standardize_brightness(src_rgb)
        stain_src = get_stain_matrix_macenko(src_rgb, Io=self.Io)
        od = rgb_to_od(src_rgb, Io=self.Io).reshape((-1, 3))

        C_src, _, _, _ = np.linalg.lstsq(stain_src.T, od.T, rcond=None)
        C_src = C_src.T

        mu_src = np.mean(C_src, axis=0)
        sigma_src = np.std(C_src, axis=0)
        sigma_src[sigma_src == 0] = 1.0

        C_norm = (C_src - mu_src) / sigma_src
        C_norm = C_norm * self.sigma_tgt + self.mu_tgt

        od_norm = C_norm @ self.stain_tgt
        od_img = od_norm.reshape(src_rgb.shape)
        return od_to_rgb(od_img, Io=self.Io)

# =========================================================
# 3) H/E maps con Ruifrok–Johnston
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
# 5) TARGET: scegli manualmente gli indici target
#    (necessario per Macenko)
# =========================================================
tgt_indices = [XXX]  # <-- MODIFICA QUI, NEL NOSTRO CASO LA NUM. 2172

# =========================================================
# 6) Esperimento: sorgenti = TUTTO il dataset
# =========================================================
N_total = images_np.shape[0]
src_indices = list(range(N_total))

rows = []

for tgt_idx in tgt_indices:
    tgt_rgb = images_np[tgt_idx]

    mac = MacenkoNormalizer()
    mac.fit(tgt_rgb)

    for src_idx in src_indices:
        src_rgb = images_np[src_idx]
        norm_rgb = mac.transform(src_rgb)

        m = compute_metrics(norm_rgb, tgt_rgb)
        m["tgt_idx"] = int(tgt_idx)
        rows.append(m)

df = pd.DataFrame(rows)


# =========================================================
# 7) OUTPUT: mostra SOLO media e std (no singole immagini)
# =========================================================

print("\n=== Summary OVERALL (mean ± std) su tutte le sorgenti e tutti i target ===")
summary_overall = df[["rRMSE_mean", "Pearson_mean", "QSSIM_mean"]].agg(["mean", "std"])
display(summary_overall)
