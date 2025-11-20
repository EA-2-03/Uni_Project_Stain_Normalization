import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# ------------------------------
# Converte immagine RGB in Optical Density (OD)
# OD = -log(I / Io)   dove Io ~ intensità della luce incidente
# ------------------------------
def rgb_to_od(image_rgb, Io=240.0):
    image_rgb = image_rgb.astype(np.float32)
    image_rgb[image_rgb == 0] = 1  # evita log(0)
    return -np.log(image_rgb / Io)

# ------------------------------
# Converte OD → RGB (formula inversa di sopra)
# ------------------------------
def od_to_rgb(od, Io=240.0):
    return np.clip(Io * np.exp(-od), 0, 255).astype(np.uint8)

# ------------------------------
# Stima la stain matrix con il metodo Macenko
# 1. Converte in OD
# 2. Rimuove lo sfondo (beta)
# 3. PCA per ottenere piano colore 2D
# 4. Angoli estremi → vettori H e E
# ------------------------------
def get_stain_matrix_macenko(image_rgb, Io=240.0, beta=0.15, alpha=1):
   
    # Converti in OD e appiattisci in N×3
    od = rgb_to_od(image_rgb, Io=Io).reshape((-1, 3))

    # Maschera: tieni solo pixel sufficientemente "scuri" (non sfondo)
    mask = np.any(od > beta, axis=1)
    od_fg = od[mask]

    # PCA per ridurre OD a uno spazio 2D
    pca = PCA(n_components=2)
    od_proj = pca.fit_transform(od_fg)  
    eigvecs = pca.components_.T    # vettori propri principali (3×2)

    # Angolo di ogni punto nella proiezione 2D
    phi = np.arctan2(od_proj[:, 1], od_proj[:, 0])

    # Prendi gli angoli estremi per stimare i vettori stain
    min_phi = np.percentile(phi, alpha)
    max_phi = np.percentile(phi, 100 - alpha)

    # Ricostruisci i vettori stain in OD 3D
    v1 = np.dot(eigvecs, [np.cos(min_phi), np.sin(min_phi)])
    v2 = np.dot(eigvecs, [np.cos(max_phi), np.sin(max_phi)])

    # Normalizza i vettori H e E
    H = v1 / np.linalg.norm(v1)
    E = v2 / np.linalg.norm(v2)

    stain_matrix = np.vstack([H, E])  # matrice 2×3
    return stain_matrix

# ------------------------------
# Risolve OD = C × stain_matrix  → C = concentrazioni dei due stain
# ------------------------------
def get_concentrations(image_rgb, stain_matrix, Io=240.0):
 
    # Converti immagine in OD
    od = rgb_to_od(image_rgb, Io=Io).reshape((-1, 3))
    
    # Risoluzione ai minimi quadrati (pinv equivalente)
    C, _, _, _ = np.linalg.lstsq(stain_matrix.T, od.T, rcond=None)
    return C.T   # forma (N,2)

# ------------------------------
# CARICAMENTO IMMAGINI
# ------------------------------

# Immagine da normalizzare (source)
source_bgr = cv2.imread("percorso_immagine_sorgente")
source_rgb = cv2.cvtColor(source_bgr, cv2.COLOR_BGR2RGB)

# Immagine target (colore di riferimento)
target_bgr = cv2.imread("percorso_immagine_target")
target_rgb = cv2.cvtColor(target_bgr, cv2.COLOR_BGR2RGB)

# ------------------------------
# STIMA STAIN MATRIX DI SOURCE E TARGET
# ------------------------------
stain_src = get_stain_matrix_macenko(source_rgb)
stain_tgt = get_stain_matrix_macenko(target_rgb)

# ------------------------------
# ESTRAZIONE CONCENTRAZIONI DALLE DUE IMMAGINI
# ------------------------------
C_src = get_concentrations(source_rgb, stain_src)   # concentrazioni source
C_tgt = get_concentrations(target_rgb, stain_tgt)   # concentrazioni target

# ------------------------------
# CALCOLO STATISTICHE DELLE CONCENTRAZIONI
# Normalizzazione stile z-score verso il target
# ------------------------------
mu_tgt = np.mean(C_tgt, axis=0)
sigma_tgt = np.std(C_tgt, axis=0)

mu_src = np.mean(C_src, axis=0)
sigma_src = np.std(C_src, axis=0)

# Per sicurezza: evita divisioni per zero
sigma_src[sigma_src == 0] = 1.0

# ------------------------------
# NORMALIZZAZIONE DELLE CONCENTRAZIONI
# Porta le concentrazioni del source nella distribuzione del target
# ------------------------------
C_src_norm = (C_src - mu_src) / sigma_src
C_src_norm = C_src_norm * sigma_tgt + mu_tgt  

# ------------------------------
# RICOSTRUZIONE DELL’IMMAGINE NORMALIZZATA
# OD_norm = C_norm × stain_target
# ------------------------------
od_norm = np.dot(C_src_norm, stain_tgt)  
od_norm_img = od_norm.reshape(source_rgb.shape)

# Converte OD → RGB
img_reconstructed = od_to_rgb(od_norm_img)

# ------------------------------
# VISUALIZZAZIONE
# ------------------------------
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(source_rgb)
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(img_reconstructed)
plt.title("Macenko Normalized")
plt.axis("off")

plt.tight_layout()
plt.show()
