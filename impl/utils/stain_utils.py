# Funzioni base per il funzionamento del codice
# Posizionare il file in una cartella utils dentro la cartella contenente il codice sorgente

def RGB_to_OD(I):
    I = I.astype(np.float32)
    I[I == 0] = 1  # evita log(0)
    return -np.log(I / 255.0)

def OD_to_RGB(OD):
    return (255 * np.exp(-OD)).astype(np.uint8)

def normalize_rows(A):
    return A / np.linalg.norm(A, axis=1, keepdims=True)

def standardize_brightness(I):
    I = I.astype(np.float32)
    p = np.percentile(I, 95)
    return np.clip(I * 255.0 / p, 0, 255).astype(np.uint8)

def notwhite_mask(I, thresh=0.8):
    return np.min(I, axis=2) < (thresh * 255)

def get_concentrations(I, stain_matrix):
    OD = RGB_to_OD(I).reshape((-1, 3))
    concentrations, _, _, _ = np.linalg.lstsq(stain_matrix.T, OD.T, rcond=None)
    return concentrations.T

