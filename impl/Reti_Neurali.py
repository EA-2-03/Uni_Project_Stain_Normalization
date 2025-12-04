# SOLO LA PRIMA VOLTA: clonare il repo e installare le dipendenze
!git clone https://github.com/khtao/StainNet.git

# Entrare nella cartella del repo
%cd StainNet

import os
import sys
import numpy as np
import torch
import torch.nn as nn
import cv2
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. Impostazioni di base
# --------------------------------------------------

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Device:", device)

# Percorso al fold 2 di PanNuke (images.npy)
# 🔴 CONTROLLA che questo percorso sia corretto nel tuo pc
pannuke_path = "percorso_images.npy"

# Carica il file numpy
images_np = np.load(pannuke_path)
print("Shape PanNuke:", images_np.shape, "dtype:", images_np.dtype)


if images_np.dtype != np.uint8:
    images_np = np.clip(images_np, 0, 255).astype(np.uint8)

# Scegli un indice (per esempio 80)
idx = 80
src_rgb = images_np[idx]        # shape (256,256,3), già RGB nel file PanNuke
print("Shape immagine scelta:", src_rgb.shape)

# --------------------------------------------------
# 2. Import del modello StainNet dal repo
# --------------------------------------------------

# Siamo già dentro la cartella StainNet se hai fatto "%cd StainNet"
# In caso contrario, decommenta:
# %cd /percorso/alla/cartella/StainNet

import sys

stainnet_path = "percroso_cartella_StainNet"
sys.path.append(stainnet_path)

print("Aggiunta cartella:", stainnet_path)


# ⚠️ Apri models.py nel repo e verifica il nome della classe.
# Nella maggior parte dei fork il modello si chiama "StainNet" o simile.
from models import StainNet  # <-- se il nome è diverso, cambialo qui

# Crea l’istanza del modello.
# I parametri (input_nc, output_nc, channels, n_layer) sono presi dalla README;
# Controlla in models.py che coincidano, altrimenti adatta.
net = StainNet(
    input_nc=3,
    output_nc=3,
    n_channel=32,
    n_layer=3
).to(device)

net.eval()

# --------------------------------------------------
# 3. Carica i pesi pre-addestrati
# --------------------------------------------------

# 🔴 QUI devi mettere il percorso ESATTO al file .pth dentro "checkpoints"
#   - apri la cartella StainNet/checkpoints nel tuo PC
#   - guarda il nome del modello (es. "StainNet_camelyon16.pth" o simile)
#   - sostituisci la stringa qui sotto
model_path = os.path.join("checkpoints", "percorso_al_modello") #nel percorso al modello escludere checkpoints perché messo prima

state = torch.load(model_path, map_location=device)

# Alcuni modelli salvano direttamente lo state_dict, altri in un dict con chiave 'state_dict'
if isinstance(state, dict) and "state_dict" in state:
    net.load_state_dict(state["state_dict"])
else:
    net.load_state_dict(state)

print("Pesi caricati da:", model_path)

# --------------------------------------------------
# 4. Funzione di normalizzazione con StainNet
# --------------------------------------------------

def normalize_with_stainnet(img_rgb: np.ndarray) -> np.ndarray:
    """
    img_rgb: numpy array HxWx3 in RGB, uint8 [0..255]
    ritorna: numpy array HxWx3 normalizzata RGB, uint8 [0..255]
    """
    # converte in float32 [0,1]
    img = img_rgb.astype(np.float32) / 255.0
    # (H,W,3) -> (1,3,H,W)
    img_t = torch.from_numpy(img.transpose(2, 0, 1)).unsqueeze(0).to(device)

    with torch.no_grad():
        out_t = net(img_t)

    # output presumibilmente in [0,1] (controlla in demo.ipynb se è diverso)
    out = out_t.squeeze(0).cpu().numpy().transpose(1, 2, 0)
    out = np.clip(out, 0.0, 1.0)
    out_uint8 = (out * 255).astype(np.uint8)
    return out_uint8

# --------------------------------------------------
# 5. Applica StainNet all’immagine sorgente
# --------------------------------------------------

src_norm = normalize_with_stainnet(src_rgb)

# --------------------------------------------------
# 6. Visualizza a schermo: sorgente vs normalizzata
# --------------------------------------------------

plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.imshow(src_rgb)
plt.title("Immagine Sorgente")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(src_norm)
plt.title("StainNet Normalized")
plt.axis("off")

plt.tight_layout()
plt.show()
