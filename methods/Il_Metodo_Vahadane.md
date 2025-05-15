Link della fonte delle informazioni:[https://ieeexplore.ieee.org/abstract/document/7460968]  {RICERCA DI AGOSTO 2016}

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
In questa ricerca, viene confrontata la separazione basata sulla fattorizzazione SNMF con il metodo basato sulla fattorizzazione NMF e con il metodo basato sulla SVD. La ICA non è stata messa a confronto in quanto le sue performance sono molto lontane da quelle riscontrate con la NMF e la BCD. Inoltre anche la BCD non è stata messa a confronto perché nessuno dei dettagli richiesti per la sua implementazione e nessun codice sorgente sono stati resi disponibili nella ricerca di Gavrilovic. Comunque, la BCD è stata confrontata con la SNMF in base ai suoi risultati relativi alla NMF.  

### *C-->METODI DI NORMALIZZAZIONE BASATI SULLA SEPARAZIONE DELLE MACCHIE*  

Le tecniche di normalizzazione supervisionate come il metodo di Khan e il metodo di Magee sono limitate nel modellare la variazione del colore del solo dataset di training. Potrebbe essere necessaria una riqualifica per diversi tipi di tessuti, schemi di colorazione, e addirittura per lo stesso tipo di tessuto ma di diversi laboratori. In aggiunta, un'applicazione utile per la normalizzazione del colore è quella di migliorare l'aspetto del colore o il contrasto delle slide istologiche sbiadite o di bassa qualità. Risulta molto difficile per un dataset di training coprire le slide istologiche su tutti i possibili scenari.  
 - Metodo di Khan: [https://ieeexplore.ieee.org/document/6727397]
 - Metodo di Magee: [https://www.researchgate.net/publication/228855426_Colour_Normalisation_in_Digital_Histopathology_Images]  

Tra i metodi non supervisionati, il metodo Macenko usa la SVD per estrarre i vettori delle macchie seguiti dalla correzione della direzione rendendolo robusto per le variazioni tra immagini. Comunque, nel processo della normalizzazione, gli autori hanno usato un modello d'aspetto del colore integrato per modificare la distribuzione del colore di un'immagine data, il quale non è flessibile come avere l'abilità di selezionare un'immagine bersaglio con un aspetto del colore preferito da un esperto. Inoltre, le macchie modellanti come componente principale non garantisce la non-negatività o la scarsità. Per questo, le mappe dei componenti risultanti possono essere difficili da interpretare biologicamente.  

## #3.METODI  

Il metodo di separazione delle macchie proposto basato sulla normalizzazione SNMF è integrale all'algoritmo della normalizzazione SPCN. Al suo centro c'è l'aggiunta di un vincolo di scarsità nella NMF che cattura il principio biologico della discretezza delle strutture biologiche. Cioè, ogni struttura biologica, come un nucleo, ha un'estensione spaziale finita e connessa, il quale è caratterizzato da uno spettro assorbente o da macchie effettive. In questa sezione, verranno forniti dettagli sull'implementazione della fattorizzazione SNMF, della normalizzazione SPCN e di uno schema basato sulle patch per accelerare la stima della base del colore. I codici sorgenti della SNMF, della SPCN e dello schema per accelerare la stima sono disponibili per uso accademico sul sito [https://github.com/abhishekvahadane/CodeRelease_ColorNormalization.git] (codici per MatLab, non Python!!).  

### *A-->SEPARAZIONE BASATA SULLA FATTORIZZAZIONE SNMF*  

In primo luogo si converte un'immagine RGB in uno spazio di densità ottica(OD) usando la formula $V = \log(\frac{I_{o}}{I})$ basata sulla legge di Beer-Lambert. Successivamente, si aggiunge il vincolo di scarsità all'equazione $\min_{W, H}\space\frac{1}{2} \|| V - WH \||_F^2$ , proponendo così una funzione di costo NMF migliorata per la separazione delle macchie, includendo una regolarizzazione della scarsità *l1* sui coefficienti di miscelazione delle macchie *Hj*, con le macchie indicizzate per $j=1,2,...,r$, il quale porta alla somma tra  

$\min_{W, H}\space\frac{1}{2} \|| V - WH \||_F^2$   e  

$\space(\lambda \sum_{j=1}^{r})  \|| H(j, :) \||_1$, con $W, H \geq 0$ e $\|| W(:, j) \||_2^2 = 1$, dove $\lambda$ è la sparsità ed il parametro di regolarizzazione. Si noti che il vincolo addizionale su W è per sopprimere molte soluzioni equivalenti del tipo $(W/\alpha \space, \alpha H)$ , con $\alpha >0$.  
L'ottimizzazione non convessa congiunta nel vincolo $\|| W(:, j) \||_2^2 = 1$ viene risolta alternando tra W e H, ottimizzando così un set di parametri mentre si mantiene l'altro fisso , partendo con un'inizializzazione di W da elementi casuali del dataset di training (V), la densità ottica dell'RGB di due pixel selezionati casualmente corrisponde a due colonne di W nell'immagine istologica, come segue:  
 - Per W fisso, $\hat{H} = \min_{H} \space \frac{1}{2} \left\| V - \hat{W}H\right\|_F^2 + \lambda\left\|H\right\|_1$
 - Per H fisso, $\hat{W} = \min_{W} \space \frac{1}{2} \left\|V - WH\right\|_F^2$ , con $W \geq 0$ e $\|| W(:, j) \||_2^2 = 1$.  

Questa funzione di costo è equivalente con un obiettivo di apprendimento del dizionario ben stabilito, ma con vincolo non-negativi aggiuntivi negli atomi del dizionario W e nei coefficienti H. Questi due step alternativi vengono chiamati "sparse coding per H" e "dictionary learning per W" , e vengono riassunti come segue: 
 - Lo sparse coding o stima di H con $\hat{W}$ fisso è un problema dei minimi quadrati lineari regolarizzati-*l1* . Una serie di metodi recenti per risolvere questo tipo di problemi è basata su una discesa coordinata con soglia morbida e su un algoritmo LARS-LASSO. Comunque, quando le colonne del dizionario sono altamente correlate, la discesa coordinata risulta molto lenta. Da qui, viene usato il LARS con un'efficiente implementazione basata su Cholesky, la quale fornisce una soluzione robusta e accurata senza il bisogno di un criterio arbitrario.
 - Il dictionary learning o stima di W viene fatto usando la discesa coordinata a blocchi senza parametri con ripartenza a caldo, la quale non richiede la messa a punto del rateo di apprendimento continuando a garantire la convergenza a un ottimale globale per l'ottimizzazione convessa nell'equazione $\hat{W} = \min_{W} \space \frac{1}{2} \left\|V - WH\right\|_F^2$. Vengono utilizzati dei Software disponibili pubblicamente chiamati SPAMS (SPArse Modelling Software) per lo sparse coding ed il dictionary learning. Bisogna far notare, però, che anche se gli SPAMS sono ottimizzati per risolvere la funzione di costo migliorata , il consumo computazionale per un risolvitore di questo genere sarebbe troppo dispendioso essere applicato a immagini WSI di grandi dimensioni.  

### *B-->NORMALIZZAZIONE SPCN*  

Per normalizzare l'aspetto del colore dell'immagine sorgente *s* in quello dell'immagine bersaglio *t*, in primo luogo , bisogna stimare gli aspetti del colore e le mappe di densità fattorizzando $V_{s}$ in $W_{s}H_{s}$, e $V_{t}$ in $W_{t}H_{t}$ usando la fattorizzazione SNMF proposta. Successivamente, una versione scalata della mappa di densità della sorgente $W_{s}$ viene combinata con l'aspetto del colore del bersaglio $W_{t}$ invece di quello della sorgente $W_{s}$ per generare l'immagine sorgente normalizzata. Questo preserva la struttura in termini di densità H, e cambia solamente l'aspetto in termini di W, e può essere descritta come segue:  
 - $H_s^{norm}(j,:) = \frac{H_s(j,:)}{H_s^{RM}(j,:)} H_t^{RM}(j,:)$, con $j=1,..,r$  
 - $V_s^{norm} = W_t H_s^{norm}$
 - $I_s^{norm} = I_0 \exp(-V_s^{norm})$  
Qui si ha $H_i^{RM} = RM(H_{i})$ , con $i=(s,t)$ e $RM$ il calcolo robusto pseudo massimo di ogni vettore riga al 99%.  
Rispetto al mapping non-lineare tra le statistiche di $H_{s}$ e $H_{t}$ nel metodo di Khan, qui viene moltiplicato solo $H_{s}$ per uno scalare e quindi vengono mantenute intatte le mappe di densità dell'immagine sorgente. Questa tecnica è simile al metodo Macenko dove le mappe di coefficienti misti dei principali componenti vengono preservate per l'immagine sorgente. In questo modo, una volta che la separazione è stata fatta in maniera accurata, la tecnica di normalizzazione di Vahadane cambia solo l'aspetto del colore (la base) mentre preserva le struttura della sorgente. Questa proprietà che preserva la struttura viene validata nella sezione #4B per la sua utilità. Ai tempi della ricerca di Vahadane, è stata la prima volta che la conservazione della struttura viene considerata simultaneamente sia nella separazione delle macchie che nella normalizzazione. Tentativi precedenti nella separazione delle macchie (per esempio Macenko), non partono con proprietà strutturali delle macchie come la scarsità e la non-negatività e quindi non sempre garantiscono invarianza strutturale dopo la normalizzazione.  

### *C-->SCHEMA PER ACCELERARE LA STIMA NELLE IMMAGINI WSI BASATO SULLE PATCH  

Come spiegato nelle sezioni 3A e 3B, la maggior parte del tempo di calcolo di una normalizzazione SPCN viene impiegato nell'ottimizzazione iterativa della fattorizzazione SNMF, la quale rallenta le sue performance nelle WSI, specialmente quando la RAM di un computer è limitata rispetto alle dimensioni delle WSI. Quindi, lo schema proposto aiuta in questo caso. Lo schema stima la matrice d'aspetto globale W di una WSI basato su un campionamento di smart patch e sulla separazione delle macchie a chiazze. Le patch hanno la stessa risoluzione dell'immagine WSI originale per preservare le strutture locali, in quanto potrebbero essere perse usando il sottocampionamento, una banale alternativa.  
Per iniziare, si campionano le patch centrate nei punti angolari della griglia e si scartano quelli che giaciono nello spazio bianco confrontando la loro luminosità con una soglia (intorno allo 0.9). La luminosità è il valore L nello spazio di colore $L * a * b$. Poi, si stimano le matrici della base del colore $W_{i}$ per ognuna delle patch campionate indicizzandole per i usando la SNMF. Le macchie di colore delle colonne nella $W_{i}$ sono ordinate in base all'intensità del canale blu, facendo sì che la prima colonna corrisponda alla hematoxylina e la secondo all'eosina. Per ultimo, si prende la mediana di queste matrici elemento per elemento per rendere la stima del colore più robusta agli artefatti come la piegatura, la sfocatura o i buchi. Da qui si normalizza la matrice mediana per avere le colonne vettoriali unitarie, e denotare la matrice finale W così ottenuta. La scelta della griglia e della grandezza delle patch sarà spiegata nelle sezioni 4 e 5.  
La separazione delle macchie per le WSI si ottiene attaverso la deconvoluzione del colore:  $H = W^{+}V$, con $H\geq 0$ e con $W^{+} = (W^{T}W)^{-1}W^{T}$ la matrice pseudo-inversa di W. Questa operazione si può anche fare separatamente per sotto-immagini delle WSI, basta usare una matrice per l'aspetto del colore singolo W, ottenuta per l'intera immagine e ,ottenendo H tramite la pseudo-inversa, si può tenere per ogni sotto-immagine e quindi si può paralizzare.  
Dopo la separazione delle macchie delle WSI sorgente e di quelle bersaglio, rispettivamente $V_{s} = W_{s} H_{s}$ e $V_{t} = W_{t} H_{t}$, bisogna cambiare l'aaspetto del colore delle WSI sorgente in quello delle WSI bersaglio ma bisogna anche preservare la concentrazione delle macchie originale per ottenere le WSI sorgente normalizzate.  

## 4.ESPERIMENTI E RISULTATI  

La separazione basata su SNMF e la normalizzazione SPCN sono state testate ampiamente, sia da un lato qualitativo che da un lato quantitativo. Tutti i dataset usati per i test durante la ricerca sono dati di riferimento disponibili pubblicamente, e consentono un facile e giusto confronto con altri metodi concorrenti.  

### *A-->PERFORMANCE DELLA SEPARAZIONE DELLE MACCHIE DELLA SNMF  

La SNMF è stata quantitativamente validata contro le separazioni basate sulla NMF e sulla SVD in base ai test sui campioni di quattro diversi tipi di tessuti: stomaco, prostata, colon e vescica, tutti disponibili nel portale dati 'The Cancer Genome Atlas(TCGA)' . La deconvoluzione BCD non fornisce codice sorgente di accesso pubblico e per questo si possono solo riportare i loro risultati e fare un confronto con la NMF.  
 - Generazione della verità di base: Mentre molte idee sono state proposte per generare la verità di base per le mappe di densità e i loro modelli di aspetto del colore, come le slide di scansione con macchie pure (metodo di Rabinovich), il [metodo di Ruifrok](methods/Il_Metodo_di_Ruifrok_Johnston.md) o lo scanning di una singola sezione di tessuto usando la decolorazione chimica. Questi metodi portano a errori a causa di perdità di macchie e co-locazione, come la presenza a livello base di eosina anche in aree coperte primariamente da hematoxylina. Secondo Vahadane, le idee proposte nel metodo di Gavrilovic sono le più vicine a catturare la reale manifestazione degli aspetti delle macchie nel contesto delle strutture di tessuti reali. Seguendo questo approccio, gli esperti del team di Vahadane hanno marcato un sottoinsieme di regioni di tessuto che devono essere colorate dall'hematoxylina separatamente dal sottoinsieme che deve essere colorato dall'eosina in $*n*$ patch non sovrapposte selezionate casualmente, le patch hanno una dimensione di 1000x1000 per ogni tipo di tessuto (per quanto riguarda la dimensione di un microscpico campo di vista (FOV), ogni FOV copre un'area fisica di circa $0.25mm\space x\space 0.25mm \space =\space 0.0625 mm^2 $ ) . La mediana dei pixel selezionati da ogni macchia per ogni FOV in uno spazio RGB forma la base del colore ($I_{k}^{median}$) per questa macchia e per il FOV (mediana in uno spazio RGB che aiuta a filtrare il rumore on relativo alla macchia come piccola polvere o buchi) e la mediana di tutti gli $*n*$ FOV ha formato la base del colore della verità di base ($I_{gt}^{median}$) per questo particolare tessuto. La $W_{k}$ e la $W_{gt}$ corrispondondenti a $I_{k}^{median}$ e a $I_{gt}^{median}$ vengono calcolate dalla formula $I = I_0 \exp(-W H)$ seguite dalla normalizzazione di ogni vettore colonna all'unità. La varianza di $W_{k}$ in tutti i FOV può essere attribuita alla variazione della qualità delle macchie nelle sezioni di tessuto e alla variazione intra-patologa. Data la matrice d'aspetto del colore , la densità delle macchie può essere generata usando il metodo della deconvoluzione del colore: $H_{gt} = (W_{gt}^T W_{gt})^{-1} W_{gt}^T V$ .  
Inoltre si possono usare le stesse metriche di confronto per valutare la separazione delle macchie del metodo di Vahadane. 

















 












































