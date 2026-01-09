# METODI DI NORMALIZZAZIONE DELLE IMMAGINI H&E
In questo progetto troverete delle ricerche sui vari metodi di normalizzazione delle immagini, in questo caso in ambito medico. Il traguardo di questo progetto è trovare il miglior (o uno dei migliori) metodo per normalizzare le immagini; gli attributi fondamentali di un buon metodo sono alta affidabilità, riproducibilità e accuratezza nella diagnosi.  
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
      - [Immagine prima e dopo la normalizzazione](Immagini/Norm_Reti_neurali/Diff_Prima_Dopo_RetiNeurali.png)




Per vedere le differenze visive tra i vari metodi, ho messo a confronto i vari output, tutti in un unica [immagine](Immagini/Confronto_metodi.png) .

## OBIETTIVI DEL PROGETTO E SPIEGAZIONE DELLE SCELTE

L'obiettivo principale di questo progetto è sicuramente trovare il metodo migliore, se non i migliori, per normalizzare le immagini. Per fare questo, i vari metodi devono avere qualcosa per essere confrontati. 
Vahadane , durante il suo lavoro, ci mostra già un confronto fatto tra il suo metodo, il metodo Macenko e il metodo di Reinhard. Ha utilizzato tre metriche principalmente:
1. rRMSE (Errore Quadratico Medio relativo) --> è un indicatore statistico fondamentale per valutare l'accuratezza di un modello di previsione o di stima; in questo caso la formula della rRMSE è $\text{rRMSE} = \frac{\|| I_{normalizzata} \space -I_{target} \space \||}{\||I_{target}\space \||}_2$ ; minore sarà l'errore, migliore sarà l'accuratezza del metodo .
2. correlazione di Pearson (con coefficiente $r$ )--> è uno degli indici statistici più utilizzati per misurare la relazioni tra due variabili; il coefficiente oscilla tra -1 e +1, con valori di +1 si ha una correlazione positiva perfetta, con -1 una correlazione negativa perfetta e con 0 assenza di correlazione; più il coefficiente si avvicina a +1 , maggiore sarà la correlazione e  di conseguenza migliore sarà il metodo .
3. QSSIM (indice di somiglianza strutturale del quaternione) --> il QSSIM è un'estensione matematica del SSIM (indice di somiglianza strutturale) progettata per valutare la qualità delle immagini a colori trattandole come entità vettoriali; trattando ogni pixel come un quaternione , il QSSIM cattura non solo le variazioni di luminanza e contrasto, ma anche le distorsioni nelle relazioni cromatiche (fase e saturazione); come nel caso della correlazione di Pearson si ha un valore che oscilla tra +1 e -1 , che vicino a +1 va a dire un risultato migliore ; viene applicato molto spesso per quanto riguarda l’Intelligenza Artificiale in quanto supporta la valutazione di sistemi AI che generano o elaborano immagini, garantendo che le informazioni visive critiche siano preservate.
In questo progetto abbiamo ampliato il confronto tramite queste tre metriche a tutti i metodi coinvolti. 

Il dataset PanNuke è stato scelto perché soddisfa alcuni punti chiave per quanto riguarda la scelta di un metodo di normalizzazione efficace . 
Alcuni punti fondamentali: 
- Eterogeneità e variabilità genetica --> PanNuke contiene campioni di tessuti di 19 organi diversi ; un buon metodo di normalizzazione deve saper normalizzare immagini con diverse texture tessutali e diverse densità cellulari .
- Variabilità inter-laboratorio --> le immagini del dataset derivano dal TCIA (The Cancer Imaging Archive) , il che significa che le slide sono state digitalizzate con scanner diversi, con protocolli di colorazione diversi e in centri diversi; PanNuke offre il "terreno di prova" ideale per ottenere lo scopo della normalizzazione (eliminare le variazioni introdotte dal processo di colorazione) , grazie al suo rumore intrinseco e alle variazioni di contrasto e saturazione già presenti .
- Presenza di classi cellulari multiple --> PanNuke offre 5 tipi diversi di cellule (neoplastiche, infiammatorie, connettive, morte e epiteliali sane); grazie a questa varietà di classi cellulari , si comprende se un metodo di normalizzazione preserva i tratti semantici dell'immagine qualsiasi sia la sua classe cellulare .
- Benchmark moderno e citabilità --> PanNuke è uno dei dataset più recenti (2019) e completi nel panorama della patologia digitale .


Per ottenere dei confronti, prima abbiamo creato un codice per un primo metodo,il quale mostra a schermo i risultati di ogni metrica prendendo randomicamente più immagini dal dataset(nel nostro caso tutto il dataset come Gold Standard , ma funziona anche con meno immagini) , poi si è creato un codice per tutti gli altri 4 metodi e ,infine , i risultati sono stati confrontati .
In sequenza i codici utilizzati nei vari metodi:
- [Macenko](impl/Metriche_Macenko.py)
- [Vahadane](impl/Metriche_Vahadane.py)
- [Ruifrok](impl/Metriche_Ruifrok.py)
- [Reinhard](impl/Metriche_Reinhard.py)
- [StainNet](impl/Metriche_StainNet.py)

Per i primi 4 metodi, essendo metodi convenzionali, è necessario avere un'immagine target, che in questo caso viene scelta tramite un calcolo matematico:
- si convertono le immagini da RGB a uno spazio Lab
- si calcola la media dei singoli canali (L,a,b) in tutto il dataset
- si calcola la distanza Euclidea D tra la media della singola immagine ($V_{img}$) e la media globale ($V_{globale}$)
- tramite la seguente formula $\space D = \sqrt{(L_{img} - L_{global})^2 + (a_{img} - a_{global})^2 + (b_{img} - b_{global})^2}$ si può trovare l'immagine target , ovvero quella con D minore (nel nostro caso abbiamo la numero 2172)

Per il metodo con StainNet , invece, bisogna prima caricare i pesi già addestrati e dopo si procede con la normalizzazione .

![image](<img width="1974" height="1176" alt="image" src="https://github.com/user-attachments/assets/f757a71d-09d5-48c2-89c2-ea11bacd2724" />)

