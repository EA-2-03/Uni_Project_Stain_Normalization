Link della fonte delle informazioni:[https://ieeexplore.ieee.org/abstract/document/7460968]  {AGOSTO 2016}

### SOMMARIO  

Il metodo di Vahadane cerca di combattere un fenomeno fisico nel quale i campioni vengono colorati solo in alcune macchie e dove molte regioni del tessuto sono caratterizzate solo da un colore efficace, questo lo fa modellandolo. Inizialmente decompone le immagini in mappe di densità delle macchie, le quali sono sparse e non negative. Per un'immagine data, le mappe vengono combinate con una base di colore di un'immagine bersaglio preferita dal patologo, così facendo si altera il suo colore mentre si conserva la sua struttura , la quale viene descritta nelle mappe.  
La correlazione della densità delle macchie con la verità di base e la preferenza dei patologi risulta maggiore con il metodo di Vahadane rispetto che con altri metodi. Inoltre, questo metodo propone un'estensione computazionalmente più veloce di questa tecnica per immagini (Whole Slide Immage) grandi, in quanto seleziona un campione appropriato di patch invece di usare l'intera immagine per calcolare la base del colore della macchia.   

## INTRODUZIONE

Il metodo di Vahadane propone una soluzione per la separazione delle macchie e la normalizzazione del colore, la quale preserva le informazioni della struttura biologica modellando le mappe di densità basandosi sulle proprietà seguenti:  
 - *Non-negatività* : E' essenziale assumere che la densità delle macchie e la sua densità ottica associata possono entrambe essere assenti(zero) o presenti(positive) in una determinata zona(pixel), ma NON POSSONO ESSERE NEGATIVE. Densità negativa vorrà dire emettere luce.
 -  *Scarsità* : Si assume che il tessuto dietro la maggior parte dei pixel rappresenta uno dei pochi tipi di materiali biologici (come i nuclei o il citoplasma),caratterizzati dalle loro macchie efficaci, permettendo a ogni pixel di essere modellato come un mix sparso di macchie efficaci constituenti. Una struttura biologica, come un nucleo, può legare più di una macchia chimica, come nel caso della colorazione H&E, ma si assume che le loro proporzioni relative sono fissate per una data struttura biologica all'interno di un'immagine. Così facendo, questo mix di macchie che è unicamente presente in un tipo di struttura biologica si può definire macchia efficace. Quindi si possono stimare i vettori di base della macchia efficace e non i vettori di base della pura macchia.
 -  *Soft-classification* : Permettendo di catturare più di una macchia a una piccola percentuale di pixel sui confini(bordi) di due materiali biologici, si possono rendere più fluide le funzioni per ottimizzare i costi.  
Per fare questo , in primo luogo si lancia il problema della separazione delle macchie come una Fattorizzazione della Matrice Non-negativa (NMF),alla quale si aggiunge un vincolo di scarsità, riferendosi ad esso come una Fattorizzazione della Matrice Non-negativa Scarsa (SNMF). Un vantaggio aggiuntivo di questa formulazione è che la base del colore è determinata in una maniera non supervisionata senza richiesta di annotazione manuale delle diverse aree di macchie pure. In questo metodo la normalizzazione del colore è costruita sulla separazione delle macchie basata su SNMF, ed è chiamata Normalizzazione del Colore Preserva-Struttura (SPCN). La SPCN funziona sostituendo la base del colore di un'immagine sorgente con quella di una bersaglio preferita dai patologi, mentre mantiene le concentrazioni della macchia originale. La flessibilità nel selezionare un aspetto del bersaglio preferito in diversi scenari rispetto a un modello di aspetto del colore del bersaglio fisso è un altro vantaggio di questa tecnica al contrario di altri metodi come, per esempio, il metodo Macenko. L'informazione sulla maggior parte delle strutture biologiche è catturato nella concentrazione delle macchie e di conseguenza con la tecnica proposta viene mantenuta. Per ultimo, questo metodo propone uno schema di stima prototipo del colore molto veloce per grandi immagini WSI, in quanto usa un campione di patch adattiva invece dell'intera immagine.  
Il gruppo di ricerca di Vahadane ha comparato quantitativamente e qualitativamente i propri algoritmi con tecniche concorrenti basate sempre sulla separazione delle macchie. Alcune di queste tecniche sono il metodo Macenko, lo studio di Gavrilovic e lo studio di Rabinovich.  
 - Metodo Macenko: [Descrizione del metodo](methods/Il_Metodo_Macenko.md)
 - Studio di Gavrilovic: [https://ieeexplore.ieee.org/document/6410037]
 - " di Rabinovich: [https://www.researchgate.net/publication/221617726_Unsupervised_Color_Decomposition_Of_Histologically_Stained_Tissue_Samples]

Per il confronto quantitativo, Vahadane e colleghi hanno generato la verità di base facendo annotare le regioni delle diverse macchie ai patologi, e usandole per calcolare la base della mediana del colore e le mappe di densità per le macchie. Inoltre hanno convalidato i metodi di separazione delle macchie confrontando la base del colore stimato e le mappe di densità con la verità di base. Oltre questo, hanno confrontato la valutazione soggettiva dei patologi della NMF e della SNMF. La SNMF ha avuto significativamente una migliore performance rispetto alla NMF, convalidando così il ruolo della scarsità nella stima della densità delle macchie. In aggiunta, la SNMF è risultata robusta alle variazioni di un superparametro nel range definito per controllare la scarsità.  
Fu confrontata quantitativamente e qualitativamente anche la SPCN basata su SNMF con altre tecniche di normalizzazione e i risultati furono dalla parte di Vahadane. Con questa tecnica si riscontra anche un aumento di velocità di 20 volte sulle WSI usando lo schema di stima dell'aspetto del colore basato sulle patch.  
Continuando in questa pagina ci saranno altre 4 sezioni fondamentali per comprendere il metodo di Vahadane.  
 - Nella sezione #2 si discute il background e il relativo lavoro dietro il metodo proposto
 - Nella sezione #3 vengono spiegati in maniera dettagliata gli algoritmi proposti
 - Nella sezione #4 vengono mostrati i risultati di un'ampia convalida di questi algoritmi
 - Nella sezione #5 si finisce con la discussione e la conclusione  

## #2.BACKGROUND E RELATIVO LAVORO

In questa Sezione, viene esaminata la separazione delle macchie e i metodi di normalizzazione, e come le tecniche proposte si sono avvicinate successivamente alla cattura delle strutture biologiche sottostanti dei tessuti, impostando lo stage per la tecnica proposta da Vahadane.  

### *A-->Normalizzazione senza separazione delle macchie*

Un modo importante per superare la variazione indesiderata del colore nelle immagini di entità similari, è trasformare l'aspetto del colore di un'immagine sorgente in quello di un'immagine bersaglio preferita da un esperto.  
La specifica dell'istogramma in uno spazio RGB e la corrispondenza delle sue statistiche (deviazione standard e media) sono state utilizzate per normalizzare l'aspetto del colore nell'istologia dopo la trasformazione di un'immagine RGB in uno spazio di colore $l{\alpha}{\beta}$ (decorrelato). Entrambe le tecniche presuppongono che le proporzioni dei compartimenti di tessuto colorati principalmente da un particolare reagente sono le stesse in tutte le immagini già normalizzate, il quale non è una valida assunzione in quanto le proporzioni dei nuclei o degli spazi bianchi variano da immagine ad immagine. L'aspetto del colore delle slide colorate che servono da campioni calibrati è stato usato anche per modellare lo spazio di colore di un sistema di imaging. Le immagini dei tessuti da esaminare sono normalizzate per combaciare l'aspetto del colore di bersagli calibrati. Questo approccio può incorporare solo variazioni di colore a causa dei diversi scanner ma non a causa delle differenze nei reagenti e delle procedure. I metodi basati sulla separazione delle macchie superano queste sfide di larga misura.  

### *B-->Metodi di separazione delle macchie soft*

Poiché la separazione delle macchie è la stima della mappa di densità di ogni macchia, è istruttivo capire la relazione tra colori RGB e la densità delle macchie in ogni pixel. Il tessuto colorato attenua la luce in un certo spettro in base al tipo e all'ammontare delle macchie che ha assorbito. Questa relazione emerge nella legge di Beer-Lambert. Usando $I \in \mathbb{R}^{m \times n}$ come matrice delle intensità RGB, con $m=3$ il numero di canali RGB e $n$ il numero di pixel, e usando $I_{o}$ per l'intensità della luce illuminante sul campione (normalmente 255 per immagini a 8 bit). Successivamente $W \in \mathbb{R}^{m \times r}$ per identificare la matrice dell'aspetto del colore delle macchie, dove le colonne rappresentano la base del colore di ogni macchia con $r$ il numero delle macchie, e $H \in \mathbb{R}^{r \times n}$ le mappe di densità delle macchie, dove le righe rappresentano la concentrazione di ogni macchia.  
Di seguito la formula: $I = I_{o} \exp(-W H)$ .  
Ora ponendo $V$ come la relativa densità ottica(OD): $V = \log(\frac{I_{o}}{I})$ .  
Di conseguenza diventa: $V = W H$.  
Perciò data la matrice d'osservazione V, l'obiettivo è trovare la matrice d'aspetto W e la matrice H.  
La deconvoluzione del colore [https://www.researchgate.net/publication/319879820_Quantification_of_histochemical_staining_by_color_deconvolution] è uno dei metodi ampiamente più usati per separare le macchie che assorbono la luce usando la relazione tra l'ammontare delle macchie e l'assorbimento della luce dato dalla legge di Beer-Lambert. Gli autori di questa ricerca suggeriscono di misurare l'aspetto del colore delle macchie da una slide di controllo con una singola macchia per slide, la quale è una stima empirica di W. Le mappe di densità H possono essere calcolate moltiplicando la densità ottica (OD) con la pseudoinversa di Moore-Penrose della matrice W. Questo metodo basato sulla calibrazione ha una forte limitazione, in quanto è valido solo per immagini che usano la stessa colorazione e stesso protocollo di imaging mentre la variazione del colore in istologia è inevitabile come visto nella Sezione 1.  
La fattorizzazione NMF è stata usata in uno dei framework non supervisionati pioneristici per la separazione delle macchie proposta nel metodo di Rabinovich, il quale ha derivato la base del colore delle macchie per la specifica immagine. I vincoli non-negativi sulla densità delle macchie e sulla matrice d'aspetto catturano le proprietà importanti delle macchie che assorbono ma non emettono luce, creando così sia la base del colore sia la densità non-negativa. Quindi, risolve il seguente problema: $\min_{W, H} \space\frac{1}{2} \|| V - WH \||_F^2$ , con $W, H \geq 0$ .  
La stima di entrambi i fattori è un problema di ottimizzazione non-convesso che può convergere verso un ottimale locale invece che verso il globale e, di conseguenza, restituire vettori non desiderati.  
Oltre alla NMF con il metodo di Rabinovich, altri metodi popolari sono basati sull'analisi di componenti indipendenti (ICA), sulla decomposizione dei singoli valori (SVD) e sulla decomposizione del colore cieco (BCD).  
- ICA (Trahearn e co.) [https://www.researchgate.net/publication/282792139_Multi-class_stain_separation_using_independent_component_analysis]
- SVD (Macenko)  [Descrizione del metodo](methods/Il_Metodo_Macenko.md)
- BCD (Gavrilovic e co.) [https://ieeexplore.ieee.org/document/6410037]

Tramite l'uso dell'errore quadrato medio della radice relativa (rMSE) tra la base stimata del colore e la verità di base del metodo di Gavrilovic, la BCD supera la NMF di circa il 20/40 % e la ICA dalle 3 alle 5 volte. Anche se la BCD ha una buona performance, non è ancora chiaro come aggiustare alcuni dei suoi superparametri. Per esempio gli autori propongono di usare una decomposizione lineare a pezzi, invece di una lineare, nel caso di una separazione a scarso gruppo di macchie, ma senza fornire una soglia quantitativa per i criteri dei pescatori per determinare i gruppi poveri. La SVD ha una soluzione a forma chiusa che può essere calcolata in modo efficiente, anche se le sue performance si deteriorano quando le immagini contengono proporzioni irregolari di ogni macchia.  
L'aggiunta di un vincolo di scarsità alla NMF, come verrà spiegato nella sezione 3A, riduce lo spazio di soluzione e aggiunge un altro principio biologicamente concordante al modello. Una formulazione scarsa per la separazione delle macchie è stata recentemente riportata nella ricerca di Chen [https://www.researchgate.net/publication/282591195_Deep_Learning_Based_Automatic_Immune_Cell_Detection_for_Immunohistochemistry_Images] . Tuttavia, è solo un'estensione del metodo di deconvoluzione del colore e in ogni caso richiede la matrice W per essere determinata in modo sperimentale, tutto ciò limita la sua applicabilità in un dataset di immagini istologiche di grandi dimensioni con una considerabile variazione di colore. 



















