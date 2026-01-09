import numpy as np
import cv2
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
# 2) REINHARD NORMALIZATION (Lab mean/std transfer)
# =========================================================
def rgb2lab(img_rgb):
    return cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB).astype(np.float32)

def lab2rgb(img_lab):
    img_lab = np.clip(img_lab, 0, 255).astype(np.uint8)
    return cv2.cvtColor(img_lab, cv2.COLOR_LAB2RGB)

def reinhard_normalize(src_rgb, tgt_rgb):
    # consigliato mantenere coerenza di luminosità
    src_rgb = standardize_brightness(src_rgb)
    tgt_rgb = standardize_brightness(tgt_rgb)

    src_lab = rgb2lab(src_rgb)
    tgt_lab = rgb2lab(tgt_rgb)

    mean_src, std_src = np.mean(src_lab, axis=(0, 1)), np.std(src_lab, axis=(0, 1))
    mean_tgt, std_tgt = np.mean(tgt_lab, axis=(0, 1)), np.std(tgt_lab, axis=(0, 1))

    std_src[std_src == 0] = 1.0

    norm_lab = (src_lab - mean_src) / std_src
    norm_lab = norm_lab * std_tgt + mean_tgt

    return lab2rgb(norm_lab)

# =========================================================
# 3) H/E maps con Ruifrok–Johnston (per metriche)
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
# 5) TARGET: scegli manualmente (1 o più)
# =========================================================
tgt_indices = [XXXX]  # <-- qui si mette il numero dell'immagine target

# =========================================================
# 6) Esperimento: sorgenti = TUTTO il dataset
# =========================================================
N_total = images_np.shape[0]
rows = []

for tgt_idx in tgt_indices:
    tgt_rgb = images_np[tgt_idx]

    for src_idx in range(N_total):
        src_rgb = images_np[src_idx]
        norm_rgb = reinhard_normalize(src_rgb, tgt_rgb)

        m = compute_metrics(norm_rgb, tgt_rgb)
        m["tgt_idx"] = int(tgt_idx)
        rows.append(m)

df_reinhard = pd.DataFrame(rows)

# =========================================================
# 7) OUTPUT: SOLO media e std (no singole immagini)
# =========================================================
print("\n=== Summary OVERALL (mean ± std) su tutte le sorgenti e tutti i target ===")
summary_overall = df_reinhard[["rRMSE_mean", "Pearson_mean", "QSSIM_mean"]].agg(["mean", "std"])
display(summary_overall)

print("\n=== Percentuale Pearson NaN (mappe costanti) ===")
print(df_reinhard["Pearson_mean"].isna().mean())


