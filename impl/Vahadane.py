import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import DictionaryLearning

# ============================================================
#               CARICAMENTO IMMAGINE SORGENTE
# ============================================================

source_path = "percorso_immagine_sorgente"
source_bgr = cv2.imread(source_path)            # Legge immagine in BGR (OpenCV)
source_rgb = cv2.cvtColor(source_bgr, cv2.COLOR_BGR2RGB)  # Conversione a RGB
source_rgb = cv2.resize(source_rgb, (128, 128))           # Ridimensiona per velocità

plt.imshow(source_rgb)
plt.title("Immagine Sorgente")
plt.axis("off")
plt.show()

# ============================================================
#               CARICAMENTO IMMAGINE TARGET
# ============================================================

target_path = "percorso_immagine_target"
target_bgr = cv2.imread(target_path)
target_rgb = cv2.cvtColor(target_bgr, cv2.COLOR_BGR2RGB)
target_rgb = cv2.resize(target_rgb, (128, 128))

plt.imshow(target_rgb)
plt.title("Immagine Target")
plt.axis("off")
plt.show()

# ============================================================
#                 FUNZIONI PER VAHADANE
# ============================================================

def RGB_to_OD(I):
    """Converte immagine RGB in Optical Density (OD)."""
    I = I.astype(np.float32)
    I[I == 0] = 1  # evita log(0) che darebbe -inf
    return -np.log(I / 255.0)

def OD_to_RGB(OD):
    """Converte OD → RGB usando formula inversa dell'assorbimento."""
    return (255 * np.exp(-OD)).astype(np.uint8)

def normalize_rows(A):
    """Normalizza ogni riga della matrice A (serve per normalizzare i vettori stain)."""
    norms = np.linalg.norm(A, axis=1, keepdims=True)
    norms[norms == 0] = 1          # evita divisione per zero
    return A / norms

def standardize_brightness(I):
    """Normalizza la luminosità portando il 95° percentile a 255."""
    I = I.astype(np.float32)
    p = np.percentile(I, 95)
    if p == 0:
        return np.clip(I, 0, 255).astype(np.uint8)
    return np.clip(I * 255.0 / p, 0, 255).astype(np.uint8)

def notwhite_mask(I, thresh=0.8):
    """Maschera dei pixel non-bianchi (usata per ignorare lo sfondo)."""
    return np.min(I, axis=2) < (thresh * 255)

def get_concentrations(I, stain_matrix):
    """Risolve OD = C * stain_matrix e restituisce le concentrazioni C."""
    OD = RGB_to_OD(I).reshape((-1, 3))
    C, _, _, _ = np.linalg.lstsq(stain_matrix.T, OD.T, rcond=None)  # risoluzione ai minimi quadrati
    C = C.T  # (N, 2)
    C = np.maximum(C, 0)   # vincolo: le concentrazioni devono essere >= 0
    return C

# ============================================================
#        STIMA DELLA STAIN MATRIX (METODO VAHADANE)
# ============================================================

def get_stain_matrix_vahadane(I, threshold=0.8, n_components=2, alpha=0.1):
    """Stima la stain matrix usando Dictionary Learning (metodo Vahadane)."""

    # seleziona pixel non-bianchi
    mask = notwhite_mask(I, thresh=threshold).reshape((-1,))
    OD = RGB_to_OD(I).reshape((-1, 3))
    OD = OD[mask]

    # Se troppi pixel, sottocampiona a 10k
    if len(OD) > 10000:
        idx = np.random.choice(len(OD), 10000, replace=False)
        OD = OD[idx]

    # Dictionary learning per ottenere i vettori stain
    dl = DictionaryLearning(
        n_components=n_components,    # due componenti = H e E
        alpha=alpha,                  # regolarizzazione L1
        max_iter=1000,
        fit_algorithm='cd',
        transform_algorithm='lasso_cd',
        positive_code=True,           # vincolo positività sulle concentrazioni
        positive_dict=True,           # vincolo positività sui vettori stain
        random_state=42
    )

    D = dl.fit(OD).components_   # matrice 2×3 (stain matrix)

    # ordina i vettori stain per consistenza
    if D[0, 0] < D[1, 0]:
        D = D[[1, 0], :]

    return normalize_rows(D)

# ============================================================
#                   CLASSE NORMALIZER VAHADANE
# ============================================================

class Normalizer:
    """Normalizzatore basato sul metodo di Vahadane."""

    def __init__(self):
        self.stain_matrix_target = None   # verrà riempita dopo il fit()

    def fit(self, target):
        """Stima la stain matrix dell'immagine target."""
        target = standardize_brightness(target)
        self.stain_matrix_target = get_stain_matrix_vahadane(target)

    def transform(self, I):
        """Normalizza una immagine I verso il target."""
        if self.stain_matrix_target is None:
            raise RuntimeError("Devi chiamare fit(target) prima di transform(I).")

        I = standardize_brightness(I)

        # Stima stain matrix dell'immagine sorgente
        stain_matrix_source = get_stain_matrix_vahadane(I)

        # Stima le concentrazioni dell'immagine sorgente
        source_concentrations = get_concentrations(I, stain_matrix_source)

        # ricostruzione OD usando la stain matrix target
        OD_norm = np.dot(source_concentrations, self.stain_matrix_target)
        OD_norm = np.clip(OD_norm, 0, 3)   # evita valori estremi OD che causano artefatti
        OD_norm_img = OD_norm.reshape(I.shape)

        return OD_to_RGB(OD_norm_img)

# ============================================================
#                  ESECUZIONE NORMALIZZAZIONE
# ============================================================

normalizer = Normalizer()
normalizer.fit(target_rgb)        # <-- QUI inseriamo l'immagine target
transformed = normalizer.transform(source_rgb)

# ============================================================
#                     VISUALIZZAZIONE RISULTATI
# ============================================================

plt.imshow(transformed)
plt.title("Normalizzata (Vahadane)")
plt.axis("off")
plt.show()

comparison = np.hstack((source_rgb, transformed))   # confronto fianco a fianco
plt.imshow(comparison)
plt.title("Confronto Sorgente vs Normalizzata")
plt.axis("off")
plt.show()

