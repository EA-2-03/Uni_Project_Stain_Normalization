import cv2
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
#                 FUNZIONI DI SUPPORTO
# ============================================================

def standardize_brightness(I):
    """
    (Opzionale) Normalizza la luminosità portando il 95° percentile a 255.
    Utile se vuoi attenuare differenze di esposizione molto estreme.
    """
    I = I.astype(np.float32)
    p = np.percentile(I, 95)
    if p == 0:
        return np.clip(I, 0, 255).astype(np.uint8)
    return np.clip(I * 255.0 / p, 0, 255).astype(np.uint8)


def rgb_to_lab(img_rgb):
    """
    Converte da RGB (0-255) a Lab (spazio colore approssimato di Reinhard).
    OpenCV usa L, a, b ciascuno in [0, 255].
    """
    img_lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
    return img_lab.astype(np.float32)


def lab_to_rgb(img_lab):
    """
    Converte da Lab (float, qualsiasi range) a RGB (uint8 0-255).
    """
    img_lab = np.clip(img_lab, 0, 255).astype(np.uint8)
    img_rgb = cv2.cvtColor(img_lab, cv2.COLOR_LAB2RGB)
    return img_rgb


def reinhard_normalize(source_rgb, target_rgb, use_brightness_std=True):
    """
    Normalizzazione colore secondo Reinhard:
    1. converte source e target in Lab
    2. calcola mean/std per ciascun canale
    3. normalizza i canali del source sulle statistiche del target
    4. ritorna immagine RGB normalizzata
    """

    # (Opzionale) normalizzazione di luminosità in RGB
    source_rgb = standardize_brightness(source_rgb)
    target_rgb = standardize_brightness(target_rgb)

    # 1) RGB -> Lab
    src_lab = rgb_to_lab(source_rgb)
    tgt_lab = rgb_to_lab(target_rgb)

    # 2) mean/std canale per canale (L, a, b)
    src_flat = src_lab.reshape(-1, 3)
    tgt_flat = tgt_lab.reshape(-1, 3)

    src_mean = np.mean(src_flat, axis=0)
    src_std = np.std(src_flat, axis=0)
    tgt_mean = np.mean(tgt_flat, axis=0)
    tgt_std = np.std(tgt_flat, axis=0)

    # evita divisione per zero
    src_std[src_std == 0] = 1.0
    if not use_brightness_std:
        # se vuoi mantenere la luminanza del source, puoi fissare L
        tgt_std[0] = src_std[0]
        tgt_mean[0] = src_mean[0]

    # 3) z-score del source + riscalatura con mean/std del target
    #    (formula di Reinhard)
    src_lab_norm = (src_lab - src_mean) / src_std
    src_lab_norm = src_lab_norm * tgt_std + tgt_mean

    # 4) Lab -> RGB
    out_rgb = lab_to_rgb(src_lab_norm)
    return out_rgb
# ============================================================
#           ESEMPIO DI UTILIZZO SU SORGENTE + TARGET
# ============================================================

# Percorsi alle immagini (modifica con i tuoi)
source_path = "percorso_immagine_sorgente"
target_path = "percorso_immagine_target"

# Carica immagine sorgente (BGR -> RGB)
src_bgr = cv2.imread(source_path)
src_rgb = cv2.cvtColor(src_bgr, cv2.COLOR_BGR2RGB)

# Carica immagine target (BGR -> RGB)
tgt_bgr = cv2.imread(target_path)
tgt_rgb = cv2.cvtColor(tgt_bgr, cv2.COLOR_BGR2RGB)

# (Opzionale) ridimensiona per velocità nei test
src_rgb = cv2.resize(src_rgb, (256, 256))
tgt_rgb = cv2.resize(tgt_rgb, (256, 256))

# Normalizzazione secondo Reinhard
src_reinhard = reinhard_normalize(src_rgb, tgt_rgb)

# ============================================================
#                 VISUALIZZAZIONE CONFRONTO
# ============================================================

plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.imshow(src_rgb)
plt.title("Sorgente")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(src_reinhard)
plt.title("Reinhard Normalized")
plt.axis("off")

plt.tight_layout()
plt.show()
