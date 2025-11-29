Link della fonte delle informazioni:
[https://www.researchgate.net/publication/319879820_Quantification_of_histochemical_staining_by_color_deconvolution] {IMPLEMENTAZIONE DELLA RICERCA DI GENNAIO 2001, SVOLTA NEL 2003}

### NOTA BENE: LE TECNOLOGIE UTILIZZATE DA RUIFROK E JOHNSTON SONO "ANZIANE" , STIAMO PARLANDO COMUNQUE DI UNA RICERCA SVOLTA 22 ANNI FA, MA NONOSTANTE QUESTO NON SONO DISPONIBILI STUDI PIU' RECENTI.

## ASTRATTO

Nel 2003 Ruifrok e Johnston provano un nuovo metodo flessibile per la separazione e la quantificazione delle macchie immunoistochimiche per mezzo dell'analisi delle immagini a colori.
Un algoritmo prodotto in quegli anni permetteva la deconvoluzione delle informazioni del colore delle immagini acquisite con camere RGB, permette di calcolare il contributo di ogni macchia applicata, basato sull'assorbimento RGB specifico della macchia.
L'algoritmo è stato testato usando un set di campioni di tumore polmonare etichettato per il rilevamento del Ki-67, un antigene espresso nelle cellule proliferanti, e ricoprendo un ampio range di livelli di colorazione. La quantificazione dell'etichettatura è stata confrontata con la segmentazione basata sulle HSI (Hue Saturation Intensity, Intensità della saturazione delle tonalità) e con l'analisi manuale degli stessi campioni.
Se messi a confronto riguardo allo standard del conteggio manuale, il metodo di deconvoluzione ha performance significativamente migliori rispetto al sistema basato sulle HSI.
Il sistema di deconvoluzione mostra variabilità nella determinazione delle LI(Labeling Index, indice di etichettatura) significativamente ridotta, specialmente dei campioni di controllo altamente etichettati. 
Questo risulta in un aumento significativo della sensibilità della classificazione dei campioni con etichettatura Ki-67 aumentata senza però cambiamenti nella specificità, se confrontato al metodo basato su HSI.

## INTRODUZIONE

Molti sistemi di imaging usano la trasformazione delle informazioni delle immagini RGB in rappresentazioni di colori specifici o HSI per la segmentazione del colore. Un problema con questi sistemi sta nel fatto che classificano dei pixel come appartenenti a un certo colore basato sul contributo di ogni singola macchia, ignorando che più di una macchia può aver contribuito al colore finale. Durante la misurazione della colorazione Ki-67 nelle slide dei tumori ai polmoni nel loro laboratorio, Ruifrok e Johnston osservano che le slide scure sembrano essere sotto-conteggiate. Crenao così un sistema di deconvoluzione del colore che può separare il contributo di massimo 3 macchie dal colore finale. La separazione del contributo di diverse macchie è molto importante nei casi dove la combinazione delle macchie risulta in una colorazione molto scura, una situazione del genere può causare problemi di classificazione usando il sistema HSI. Il metodo di deconvoluzione del colore è basato sulla trasformazione ortonormale dell'immagine RGB originale, a seconda delle informazioni del colore determinate dall'utente sulle macchie usate. Il metodo concede la possibilità di determinare la densità delle macchie, anche nelle aree dove più macchie sono colocalizzate, rendendo possibile non solo determinare la superficie dell'area e l'assorbimento totale nelle aree con un colore specifico, ma anche le densità e i rapporti delle densità delle macchie in ogni area.
Dopo la deconvoluzione del colore, le immagini possono essere ricostruite separatamente per ogni macchia, e usate per la densitometria e l'analisi delle texture per ogni macchia, usando metodi di imaging standard. 
Per provare le performance del sistema di deconvoluzione del colore, sono stati confrontati i risultati dell'etichettatura Ki-67 con anticorpi MIB-1 nel tessuto tumorale polmonare analizzati con il metodo di deconvoluzione con i risultati delle analisi usando il metodo basato su HSI. Dopodiché sono state analizzate le slide con macchie di MIB-1 da campioni di cancro ai polmoni e le slide di controllo negative e positive (tessuto tumorale del seno) in più lotti di macchie, e sono stati confrontati i due approcci basati sull' imaging con l'analisi manuale.
I parametri misurati utilizzando i due sistemi sono il LI, definito come la frazione dell'area MIB-1 positiva divisa per la frazione dell'area nucleare (MIB-1 + hematoxylina), la densità ottica media (MOD) dell'area MIB-1 positiva e il 'Quickscore', ossia il prodotto tra LI e MOD. 
Queste misurazioni sono state confrontate con il punteggio manuale delle slide, il quale viene considerato lo standard. 
Le differenze nei risultati tra la deconvoluzione del colore e le HSI sono illustrate con il confronto della selezione in primo piano dei nuclei colorati di diaminobenzidina (DAB) nei tessuti di controllo positivi.

## METODI

### - CAMPIONI

Sezioni di campioni di tumore al seno e tumore ai polmoni sono state colorate per l'espressione drlla Ki-67 con anticorpi MIB-1 e cromogeni DAB.
La controcolorazione è stata realizzata con l'hematoxylina di Mayer per 3-5 minuti. 
I campioni sono stati colorati in 7 diversi lotti, 6 contenenti tumori maligni ai polmoni e 1 contenente tumori benigni ai polmoni, ognuno dei quali contiene diversi campioni di polmone, una slide di controllo positiva e una negativa. L'analisi iniziale è stata fatta tramite il metodo basato su HSI.
Da ognuno dei 6 lotti con tumori maligni, sono stati analizzati con il metodo di deconvoluzione del colore 2 campioni con punteggio basso, 2 con punteggio medio e 2 con punteggio alto, insieme ad altri 4 che sono stati segnalati durante l'analisi HSI come non affidabili e a 10 campioni benigni. Questi campioni sono stati confrontati con l'analisi manuale. 

### - ACQUISIZIONE DELLE IMMAGINI

Un microscopio Leica DMLB è stato equipaggiato con una camera Hamamatsu e interfacciato con un computer IBM equipaggiato con una scheda digitalizzatore Matrix Meteor.
Le impostazioni di luce e camera sono standard, risultando in valori di background di 20±5 (media±deviazione standard; scala 0-255 da bianco a nero) per i canali RGB.
La linearità del setup di acquisizione immagine è stato testato usando un filtro di densità neutra a gradini, trovato lineare con l'intensità della luce per tutti e tre i colori entro un 2%, in tutto il range dinamico della camera. Le immagini sono state catturate con una lenti obiettive 20x.

### - ELABORAZIONE DELLE IMMAGINI

Le immagini sono state analizzate basandosi sulle immagini HSI trasformate usando il software SAMBA IPS. Le aree di interesse sono state selezionate manualmente usando tecniche interattive copia e incolla.
Per la deconvoluzione del colore, l'immagine a 24 bit RGB sono state trasferite su un Macintosh G4 e processate e analizzate usando le immagini del NIH (National Institute of Health). 
Le macro personalizzate sono state scritte per una correzione di background e per la trasformazione da intensità a densità ottica (OD), per determinare i vettori del colore delle diverse macchie, per il calcolo della matrice di deconvoluzione del colore, e per l'effettiva deconvoluzione del colore delle immagini. Le immagini immagazzinate di un campo vuoto sono state usate per determinare la luce entrante in ogni pixel, correggendo implicitamente l'illuminazione disuguale per la sottrazione della densità ottica di background.

## ANALISI STATISTICA

I dati sono stati presentati come $media ± deviazione \space standard$ . 
La normalizzazione dei risultati di ogni lotto è stata eseguita assumendo che le slide di controllo negative incluse nello stesso lotto non abbiano effettivamente l'etichettatura Ki-67 (0%), e che le slide di controllo positive abbiano il 100% di etichettatura positiva Ki-67. 
La correlazione dei risultati dell'analisi automatizzata con il conteggio manuale è stata confrontata usando l'analissi della covarianza. Questo è stato conseguito usando l'SPSS (software sviluppato da IBM) e il programma personalizzato AOC. 

## RISULTATI

Il primo test è stato confrontare i risultati misurati per i campioni di controllo positivi e negativi in ognuno dei 7 lotti di colorazione. Una considerabile variabilità è visibile nelle misurazioni del LI, del MOD e del quickscore usando il sistema basato su HSI, con un coefficiente di variazione (CV) di quasi il 50% per il LI delle slide di controllo positive.
I dati mostrano chiaramente che la variabilità nel LI e nel quickscore è significativamente minore per la deconvoluzione rispetto al metodo basato su HSI, con un CV di solo 1% per i controlli negativi analizzati con il sistema di deconvoluzione. Solo il MOD per i controlli negativi mostra una variabilità alta con il metodo di deconvoluzione. Questa variabilità alta nel MOD può essere spiegata facilmente dalle piccole aree positive nei controlli negativi, causate da piccoli artefatti con una OD altamente variabile. Se le aree più piccole dell'area minima di un nucleo sono escluse, non si trovano aree positive misurabili nei controlli negativi.
Questi risultati spiegano che i dati HSI suggeriscono variabilità alta tra i lotti, e la normalizzazione dei dati sperimentali ai risultati di una slide di controllo positiva e di una negativa risulteranno in un cambio considerevole di valori. Comunque, il metodo di deconvoluzione mostra bassa variabilità, e cambi limitati come risultato della normalizzazione alle slide di controllo positive e negative.

Per confrontare le performance dei due approcci alle analisi con l'impressione dei patologi, sono state analizzati i risultati di 50 campioni di tumore ai polmoni coprendo tutto il range da bassa ad alta positività di Ki-67.
Gli stessi campioni sono stati conteggiati in maniera "cieca" dai patologi, analizzati usando un sistema basato su HSI, e analizzati usando il sistema di deconvoluzione. Il conteggio manuale è stato valutato lo standard del confronto. La normalizzazione ha avuto come risultato rispettivamente valori minori dello 0% e maggiori del 100% nell'etichettatura confrontati con i controlli per i dati basati su HSI.
E' chiaro sin da subito che usando i dati delle HSI la correlazione maggiore con il conteggio manuale si trova con le misurazioni con LI normalizzato, come ci si potrebbe aspettare dalla definizione del LI usata per il conteggio.
Usando il metodo di deconvoluzione, sia il LI che il quickscore danno una correlazione alta con l'analisi manuale, mentre la normalizzazione non migliora questi risultati. La correlazione del quickscore e del LI con il conteggio manuale è significativamente maggiore per il metodo di deconvoluzione rispetto al metodo basato su HSI senza normalizzazione. Dopo la normalizzazione dei dati sperimentali nei controlli inclusi, il metodo di deconvoluzione risulta sempre il migliore, anche se non significativamente per il LI.
La correlazione tra l'analisi basata su HSI e quella basata sulla deconvoluzione risulta in un $r^2$ (coefficiente di correlazione quadrato) di 0.58 per i dati LI non normalizzati e 0.74 per quelli normalizzati, leggermente maggiore ma non significativamente dopo la normalizzazione, illustrando il miglioramento con la normalizzazione tra i lotti, specialmente quando il metodo basato su HSI è in uso.

## DISCUSSIONE

- **Cosa potrebbe causare la differenza in variabilità tra il metodo basato su HSI e il metodo di deconvoluzione?**  
*Una spiegazione per l'alto tasso di errore nei controlli positivi può essere la saturazione delle macchie, causando una classificazione errata delle aree scure.
  Il metodo basato su HSI esclude i nuclei molto scuri come blu al posto del marrone; la classificazione delle HSI è molto sensibile alle impostazioni di tonalità per le aree scure, causando un'ampia variabilità nella determinazione del colore.
  Il metodo di deconvoluzione del colore non soffre di questo problema; le aree molto scure contribuiscono sia al segnale marrone che al segnale blu.*

## CONCLUSIONI

Il metodo di deconvoluzione ha performance significativamente migliori del metodo basato su HSI se confrontato col conteggio manuale come standard. La normalizzazione dei dati dalle slide di controllo positive e negative incluse in ogni lotto migliora le performance del metodo basato su HSI migliora la correlazione tra i due metodi. Il sistema di deconvoluzione mostra variabilità significativamente ridotta nella determinazione del LI in campioni di controllo etichettati. Questo risulta in un aumento sigificativo nella sensibilità di classificazione dei campioni con un etichettatura Ki-67 migliorata senza cambiare la specificità, se confrontato con il metodo basato su HSI.
