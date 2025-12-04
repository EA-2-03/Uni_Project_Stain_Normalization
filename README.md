# Uni_Project
In questo progetto troverete delle ricerche su vari metodi di normalizzazione delle immagini, in questo caso in ambito medico. Il traguardo di questo progetto è trovare il miglior (o uno dei migliori) metodo per normalizzare le immagini; gli attributi fondamentali di un buon metodo sono alta affidabilità, riproducibilità e accuratezza nella diagnosi.  
Per provare il codice prendiamo una [Immagine](Immagini/image_pre_Norm.png) campione dal Fold 2 del dataset [PanNuke](https://warwick.ac.uk/fac/cross_fac/tia/data/pannuke) .   

Esistono diversi metodi per normalizzare le immagini, tra i più utilizzati troviamo: 
- [Il Metodo Macenko]
    - [Descrizione del metodo](methods/Il_Metodo_Macenko.md)
    - [Implementazione con Python](impl/Macenko.py)
      - [Immagine prima e dopo la normalizzazione](Immagini/Norm_Macenko/Diff_Prima_Dopo_Macenko.png)
- [Il Metodo Vahadane]
    - [Descrizione del metodo](methods/Il_Metodo_Vahadane.md)
    - [Implementazione con Python](impl/Vahadane.py)
      - [Immagine prima e dopo la normalizzazione](Immagini/Norm_Vahadane/Diff_Prima_Dopo_Vahadane.png)
- [Il Metodo di Ruifrok e Johnston]
    - [Descrizione del metodo](methods/Il_Metodo_di_Ruifrok_Johnston.md)
    - [Implementazione con Python](impl/Ruifrok_Johnston.py)
      - [Immagine prima e dopo la normalizzazione](Immagini/Norm_Ruifrok/Diff_prima_dopo_Ruifrok.png)
- [Il metodo Reinhard]
    - [Descrizione del metodo](methods/Il_Metodo_Reinhard.md)
    - [Implementazione del codice](impl/Reinhard.py)
      - [Immagine prima e dopo la normalizzazione](Immagini/Norm_Reinhard/Diff_Prima_Dopo_Reinhard.png) 
- [I metodi basati sulle reti neurali]  
    - [Descrizione dei metodi](methods/I_metodi_sulle_reti_neurali.md)
    - [Implementazione con Python](impl/Reti_Neurali.py)
      - [Immagine prima e dopo la normalizzazione](Immagini/Norm_CNN/Diff_Prima_Dopo_CNN.png)




Per vedere le differenze tra i vari metodi, ho messo a confronto i vari output, tutti in un unica [immagine](Immagini/Confronto_metodi) .

