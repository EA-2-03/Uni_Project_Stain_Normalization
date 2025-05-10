#Questo codice carica e visualizza un'immagine, la converte in uno spazio OD, 
#Applica PCA per stimare due "macchie", normalizza i colori, 
#Ricostruisce l'immagine con i colori modificati, 
#Infine mostra a schermo il confronto tra immagine originale ed immagine normalizzata

import cv2  # Libreria per la gestione delle immagini (OpenCV)
import numpy as np  # Libreria per il calcolo numerico (array, operazioni matematiche)
import matplotlib.pyplot as plt  # Libreria per la visualizzazione di immagini e grafici
from sklearn.decomposition import PCA  # Algoritmo PCA (Principal Component Analysis) da scikit-learn

image = cv2.imread("Percorso_Immagine")  # Carica l'immagine dal percorso specificato (in BGR)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Converte l'immagine da BGR (OpenCV) a RGB (per Matplotlib)

plt.imshow(image_rgb)  # Visualizza l'immagine RGB
plt.title("Original Image")  # Titolo del grafico
plt.axis('off')  # Nasconde gli assi
plt.show()  # Mostra il grafico

#Viene mostrata l'immagine originale in formato RGB
#[Immagine originale](Immagini/Norm_Macenko/Prima_Norm.png)


def rgb_to_od(image_rgb):
    image_rgb = image_rgb.astype(np.float32)  # Converte i valori dei pixel in float per il calcolo
    image_rgb[image_rgb == 0] = 1  # Evita divisioni per zero
    return -np.log(image_rgb / 255)  # Converte da RGB a Optical Density (OD)
img_od = rgb_to_od(image_rgb)  # Applica la trasformazione OD all'immagine RGB

reshaped_od = img_od.reshape((-1, 3))  # Appiattisce l'immagine in una matrice N x 3 (ogni riga = pixel)
pca = PCA(n_components=2)  # Crea un oggetto PCA per ridurre da 3 a 2 componenti
pca.fit(reshaped_od)  # Applica PCA ai dati OD
stain_matrix = pca.components_.T  # Estrae i 2 principali componenti (trasposti = matrice 3x2)

stains = np.dot(reshaped_od, np.linalg.pinv(stain_matrix).T)  # Calcola le concentrazioni dei due "coloranti"
stains = stains.reshape(image_rgb.shape[0], image_rgb.shape[1], -1)  # Ricostruisce la forma originale (H x W x 2)

target_means = np.full(2, 0.5)  # Valore medio desiderato per ogni canale stain (2 componenti)
target_stds = np.full(2, 0.2)  # Deviazione standard desiderata per ogni stain
stains_normalized = (stains - np.mean(stains, axis=(0,1))) / np.std(stains, axis=(0,1))  # Normalizza i dati
stains_normalized = stains_normalized * target_stds + target_means  # Rimappa alle nuove statistiche target

od_normalized = np.dot(stains_normalized.reshape((-1, 2)), stain_matrix.T)  # Torna allo spazio OD
od_normalized = od_normalized.reshape(image_rgb.shape)  # Ricostruisce immagine in OD (forma originale)
img_reconstructed = np.exp(-od_normalized)  # Torna dallo spazio OD allo spazio RGB

img_reconstructed = np.clip(img_reconstructed, 0, 1)  # Ritaglia i valori a [0,1]
img_reconstructed = (img_reconstructed * 255).astype(np.uint8)  # Converte a interi 8-bit per visualizzazione

# Visualizzazione con matplotlib
plt.imshow(img_reconstructed)  # Mostra l'immagine ricostruita
plt.title('Reconstructed Image')  # Titolo
plt.axis('off')  # Nessun asse
plt.show()  # Mostra

#Viene mostrata l'immagine normalizzata

plt.figure(figsize=(10, 5))  # Crea una figura più larga per il confronto

plt.subplot(1, 2, 1)  # Primo pannello a sinistra
plt.imshow(image_rgb)  
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)  # Secondo pannello a destra
plt.imshow(img_reconstructed)
plt.title('Reconstructed Image')
plt.axis('off')

plt.tight_layout()  # Riduce spazi tra i grafici
plt.show()  # Mostra il confronto finale

#Viene mostrato il confronto tra l'immagine originale e quella normalizzata
