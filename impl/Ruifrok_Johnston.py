import cv2
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
#              FUNZIONI DI BASE (OD, LUMINOSITA')
# ============================================================

def rgb_to_od(I, Io=255.0):
    """Converte immagine RGB (0-255) in Optical Density."""
    I = I.astype(np.float32)
    I[I == 0] = 1  # evita log(0)
    return -np.log(I / Io)

def od_to_rgb(OD, Io=255.0):
    """Converte OD -> RGB (0-255)."""
    return np.clip(Io * np.exp(-OD), 0, 255).astype(np.uint8)

def standardize_brightness(I):
    """Normalizza la luminosità usando il 95° percentile."""
    I = I.astype(np.float32)
    p = np.percentile(I, 95)
    if p == 0:
        return np.clip(I, 0, 255).astype(np.uint8)
    return np.clip(I * 255.0 / p, 0, 255).astype(np.uint8)

def normalize_columns(M):
    """Normalizza le colonne di una matrice (norma = 1)."""
    norms = np.linalg.norm(M, axis=0, keepdims=True)
    norms[norms == 0] = 1.0
    return M / norms


# ============================================================
#          STAIN MATRIX DI RUIFROK–JOHNSTON PER H&E
# ============================================================

def get_ruifrok_he_matrix():
    """
    Restituisce la stain matrix 3x3 per H&E secondo Ruifrok & Johnston.
    Colonne = vettori OD normalizzati per H, E, e terzo stain (residuo).
    Qui usiamo il terzo vettore come prodotto vettoriale degli altri due.
    """
    # Vettori OD tipici per H & E (Ruifrok/Johnston / scikit-image)
    # (valori leggermente variabili in letteratura, questi sono standard)
    H = np.array([0.650, 0.704, 0.286], dtype=np.float32)  # Hematoxylin
    E = np.array([0.072, 0.990, 0.105], dtype=np.float32)  # Eosin

    # Terza componente = prodotto vettoriale (residuo / background)
    # in modo da formare una base 3D completa.
    D = np.cross(H, E)

    # Costruisco matrice 3x3 con colonne H, E, D
    M = np.stack([H, E, D], axis=1)   # shape (3,3)
    M = normalize_columns(M)
    return M


# ============================================================
#       CLASSE NORMALIZZATORE RUIFROK–JOHNSTON (H&E)
# ============================================================

class RuifrokJohnstonNormalizer:
    """
    Normalizzatore basato su color deconvolution di Ruifrok & Johnston.
    - Usa stain matrix fissata (H&E).
    - Decompone source e target in concentrazioni.
    - Allinea le concentrazioni H & E del source alle statistiche del target.
    """

    def __init__(self, Io=255.0):
        self.Io = Io
        self.M = get_ruifrok_he_matrix()        # stain matrix 3x3 (H, E, residuo)
        self.M_inv = np.linalg.inv(self.M)      # inversa per deconvolution
        self.mu_tgt = None
        self.sigma_tgt = None

    def _deconvolve(self, I_rgb):
        """
        Deconvolution: RGB -> OD -> concentrazioni C (N x 3).
        C[:,0] = H, C[:,1] = E, C[:,2] = terzo stain/residuo.
        """
        OD = rgb_to_od(I_rgb, Io=self.Io).reshape((-1, 3))  # (N,3)
        # Ruifrok: C = OD * M^{-1}
        C = np.dot(OD, self.M_inv)                          # (N,3)
        return C

    def _reconvolve(self, C):
        """
        Reconvolution: C (N x 3) -> OD (N x 3) -> RGB (H&E ricostruita).
        """
        OD = np.dot(C, self.M)            # (N,3)
        OD = OD.reshape(self._shape)      # salviamo shape dell'immagine
        OD = np.clip(OD, 0, 3)            # limita OD per evitare artefatti
        return od_to_rgb(OD, Io=self.Io)

    def fit(self, target_rgb):
        """
        Stima statistiche (media, std) delle concentrazioni H&E del target.
        """
        target_rgb = standardize_brightness(target_rgb)
        self._shape = target_rgb.shape

        C_tgt = self._deconvolve(target_rgb)      # (N,3)
        # prendiamo solo i primi 2 canali (H, E)
        C_tgt_he = C_tgt[:, :2]

        self.mu_tgt = np.mean(C_tgt_he, axis=0)
        self.sigma_tgt = np.std(C_tgt_he, axis=0)
        # evita std zero
        self.sigma_tgt[self.sigma_tgt == 0] = 1.0

    def transform(self, source_rgb):
        """
        Normalizza l'immagine source usando le statistiche del target.
        """
        if self.mu_tgt is None or self.sigma_tgt is None:
            raise RuntimeError("Chiama prima fit(target_rgb).")

        source_rgb = standardize_brightness(source_rgb)
        self._shape = source_rgb.shape

        # Deconvolution del source
        C_src = self._deconvolve(source_rgb)      # (N,3)
        C_src_he = C_src[:, :2]                  # componenti H & E
        C_src_rest = C_src[:, 2:]                # terzo stain (residuo)

        # Statistiche del source
        mu_src = np.mean(C_src_he, axis=0)
        sigma_src = np.std(C_src_he, axis=0)
        sigma_src[sigma_src == 0] = 1.0

        # Allinea distribuzione H&E del source a quella del target (z-score)
        C_he_norm = (C_src_he - mu_src) / sigma_src
        C_he_norm = C_he_norm * self.sigma_tgt + self.mu_tgt

        # Ricompongo le 3 componenti (H, E, residuo invariato)
        C_norm = np.concatenate([C_he_norm, C_src_rest], axis=1)  # (N,3)

        # Reconvolution per ottenere immagine RGB normalizzata
        return self._reconvolve(C_norm)

# ============================================================
#               ESEMPIO DI UTILIZZO CON DUE IMMAGINI
# ============================================================

# Percorsi alle immagini (modifica con i tuoi)
source_path = "percorso_immagine_sorgente"
target_path = "percorso_immagine_target"

# Carica sorgente
src_bgr = cv2.imread(source_path)
src_rgb = cv2.cvtColor(src_bgr, cv2.COLOR_BGR2RGB)

# Carica target
tgt_bgr = cv2.imread(target_path)
tgt_rgb = cv2.cvtColor(tgt_bgr, cv2.COLOR_BGR2RGB)

# (opzionale) ridimensiona per test veloce
src_rgb = cv2.resize(src_rgb, (256, 256))
tgt_rgb = cv2.resize(tgt_rgb, (256, 256))

# Inizializza normalizzatore Ruifrok–Johnston e fai fit sul target
rj_norm = RuifrokJohnstonNormalizer()
rj_norm.fit(tgt_rgb)

# Normalizza la sorgente
src_norm = rj_norm.transform(src_rgb)

# ============================================================
#                 VISUALIZZAZIONE CONFRONTO
# ============================================================

plt.figure(figsize=(10, 4))

# Immagine sorgente
plt.subplot(1, 2, 1)
plt.imshow(src_rgb)
plt.title("Sorgente")
plt.axis("off")

# Immagine normalizzata
plt.subplot(1, 2, 2)
plt.imshow(src_norm)
plt.title("Ruifrok–Johnston Normalizzata")
plt.axis("off")

plt.tight_layout()
plt.show()

