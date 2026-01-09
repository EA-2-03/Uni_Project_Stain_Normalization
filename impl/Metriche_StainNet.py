import numpy as np
import pandas as pd
import torch
from scipy.stats import pearsonr
from skimage.metrics import structural_similarity as ssim

# =========================================================
# 0) Caricamento PanNuke fold 2
# =========================================================
pannuke_path = "Percorso_al_file_images.npy"
images_np = np.load(pannuke_path)

if images_np.dtype != np.uint8:
    images_np = np.clip(images_np, 0, 255).astype(np.uint8)

print("Loaded:", images_np.shape, images_np.dtype)

import sys
sys.path.append("Percorso_alla_cartella_StainNet")
from models import StainNet

net = StainNet(
    input_nc=3,
    output_nc=3,
    n_channel=32,
    n_layer=3
)


device = next(net.parameters()).device

import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
net = net.to(device)

checkpoint_path = "Percorso_al_file_StainNet-Public-centerUni_layer3_ch32.pth"

state = torch.load(checkpoint_path, map_location=device)

# alcuni checkpoint hanno la chiave 'state_dict'
if isinstance(state, dict) and "state_dict" in state:
    state = state["state_dict"]

net.load_state_dict(state)
net.eval()

# =========================================================
# 1) Brightness standardization (stessa usata prima)
# =========================================================
def standardize_brightness(I):
    I = I.astype(np.float32)
    p = np.percentile(I, 95)
    if p <= 0:
        return np.clip(I, 0, 255).astype(np.uint8)
    return np.clip(I * 255.0 / p, 0, 255).astype(np.uint8)

# =========================================================
# 2) STAINNET NORMALIZATION
# =========================================================
@torch.no_grad()
def stainnet_normalize(src_rgb):
    """
    src_rgb: uint8 RGB (H,W,3)
    return: uint8 RGB (H,W,3)
    """
    src_rgb = standardize_brightness(src_rgb)

    x = src_rgb.astype(np.float32) / 255.0
    x = torch.from_numpy(x).permute(2, 0, 1).unsqueeze(0).to(device)

    y = net(x)
    y = torch.clamp(y, 0.0, 1.0)

    out = y.squeeze(0).permute(1, 2, 0).cpu().numpy()
    return (out * 255.0).astype(np.uint8)

# =========================================================
# 3) H/E maps Ruifrok–Johnston (per metriche)
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

def he_maps(img_rgb):
    od = _rgb_to_od_rj(img_rgb).reshape((-1, 3))
    C = od @ _RJ_M_INV
    H = np.clip(C[:, 0], 0, 3).reshape(img_rgb.shape[:2]).astype(np.float32)
    E = np.clip(C[:, 1], 0, 3).reshape(img_rgb.shape[:2]).astype(np.float32)
    return H, E

# =========================================================
# 4) Metriche
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

def compute_metrics(norm_rgb, ref_rgb):
    Hn, En = he_maps(norm_rgb)
    Hr, Er = he_maps(ref_rgb)

    rH = rrmse(Hn, Hr)
    rE = rrmse(En, Er)
    pH = safe_pearson(Hn, Hr)
    pE = safe_pearson(En, Er)
    sH = qssim_like(Hn, Hr)
    sE = qssim_like(En, Er)

    return {
        "rRMSE_mean": 0.5 * (rH + rE),
        "Pearson_mean": np.nanmean([pH, pE]),
        "QSSIM_mean": 0.5 * (sH + sE),
    }
# =========================================================
# 5) Esperimento: sorgenti = TUTTO il dataset
#    riferimento = immagine target scelta
# =========================================================
tgt_idx = XXXX  # numero dell'immagine target(o più)
ref_rgb = images_np[tgt_idx]

rows = []
N_total = images_np.shape[0]

for i in range(N_total):
    if i % 200 == 0:
        print(f"Processing {i}/{N_total}")

    src_rgb = images_np[i]
    norm_rgb = stainnet_normalize(src_rgb)

    m = compute_metrics(norm_rgb, ref_rgb)
    rows.append(m)

df_stainnet = pd.DataFrame(rows)


# =========================================================
# 6) OUTPUT: SOLO media e deviazione standard
# =========================================================
print("\n=== STAINNET – Summary OVERALL (mean ± std) ===")
summary = df_stainnet[["rRMSE_mean", "Pearson_mean", "QSSIM_mean"]].agg(["mean", "std"])
display(summary)

print("\n=== Percentuale Pearson NaN ===")
print(df_stainnet["Pearson_mean"].isna().mean())

