Link della fonte delle informazioni:[https://ieeexplore.ieee.org/abstract/document/7460968]  

### SOMMARIO  

Il metodo di Vahadane cerca di combattere un fenomeno fisico nel quale i campioni vengono colorati solo in alcune macchie e dove molte regioni del tessuto sono caratterizzate solo da un colore efficace, questo lo fa modellandolo. Inizialmente decompone le immagini in mappe di densità delle macchie, le quali sono sparse e non negative. Per un'immagine data, le mappe vengono combinate con una base di colore di un'immagine bersaglio preferita dal patologo, così facendo si altera il suo colore mentre si conserva la sua struttura , la quale viene descritta nelle mappe.  
La correlazione della densità delle macchie con la verità di base e la preferenza dei patologi risulta maggiore con il metodo di Vahadane rispetto che con altri metodi. Inoltre, questo metodo propone un'estensione computazionalmente più veloce di questa tecnica per immagini (Whole Slide Immage) grandi, in quanto seleziona un campione appropriato di patch invece di usare l'intera immagine per calcolare la base del colore della macchia.   

## INTRODUZIONE

Il metodo di Vahadane propone una soluzione per la separazione delle macchie e la normalizzazione del colore, la quale preserva le informazioni della struttura biologica modellando le mappe di densità basandosi sulle proprietà seguenti:  
 - *Non-negatività* : E' essenziale assumere che la densità delle macchie e la sua densità ottica associata possono entrambe essere assenti(zero) o presenti(positive) in una determinata zona(pixel), ma NON POSSONO ESSERE NEGATIVE. Densità negativa vorrà dire emettere luce.
 -  *Scarsità* : Si assume che il tessuto dietro la maggior parte dei pixel rappresenta uno dei pochi tipi di materiali biologici (come i nuclei o il citoplasma),caratterizzati dalle loro macchie efficaci, permettendo a ogni pixel di essere modellato come un mix sparso di macchie efficaci constituenti. Una struttura biologica, come un nucleo, può legare più di una macchia chimica, come nel caso della colorazione H&E, ma si assume che le loro proporzioni relative sono fissate per una data struttura biologica all'interno di un'immagine. Così facendo, questo mix di macchie che è unicamente presente in un tipo di struttura biologica si può definire macchia efficace. Quindi si possono stimare i vettori di base della macchia efficace e non i vettori di base della pura macchia.
 -  *Soft-classification* : Permettendo di catturare più di una macchia a una piccola percentuale di pixel sui confini(bordi) di due materiali biologici, si possono rendere più fluide le funzioni per ottimizzare i costi.  

