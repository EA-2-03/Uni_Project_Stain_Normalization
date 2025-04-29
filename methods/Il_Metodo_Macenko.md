Link della fonte delle informazioni:
[https://www.geeksforgeeks.org/macenko-method-for-normalizing-histology-slides-for-quantitative-analysis/]

# COSA E’ IL METODO MACENKO?

L’idea principale dietro il metodo Macenko è quella di trasformare un’immagine in uno spazio in Densità Ottica (OD), stimare i vettori delle macchie primarie usando la Decomposizione di Valori Singoli (SVD), separare l’immagine in base alle componenti delle macchie, normalizzare queste componenti in una distribuzione di riferimento, e poi ricostruire l’immagine normalizzata. Questo processo standardizza la distribuzione dei colori in slide delle macchie, facendo analisi successive più coerenti e affidabili. Nella ricerca e diagnosi medica , i colori delle immagini dei tessuti delle macchie devono essere coerenti. Diversi laboratori e procedure possono produrre immagini con colori variabili, facendo diventare così le analisi accurate più difficili da realizzare. Il metodo Macenko standardizza questi colori, assicurando coerenza in tutte le immagini. Questo processo, chiamato normalizzazione delle macchie, aiuta sia i patologi umani che i tools automatizzati nel fare valutazioni più accurate, e crea risultati più affidabili nelle ricerche e diagnosi mediche. 

## QUALI SONO LE SFIDE NEL PROCESSO DI COLORAZIONE DELLE SLIDE DI NORMALIZZAZIONE?

Diverse sfide devono essere superate a causa della grande variabilità nel processo di colorazione:
### 1. VARIABILITA' DELLA COLORAZIONE
  - Differenze di protocollo --> Diversi laboratori possono usare protocolli diversi, portando a differenza in termini di intensità di colorazione e tonalità
  - Lotti di reagenti --> La variabilità tra lotti di reagenti può influire sul colore delle macchie e sulla sua intensità 
  - Preparazione delle slide --> Le differenze nelle tecniche di preparazione delle slide possono introdurre incoerenza nella colorazione
### 2. IMPATTO NELL'ANALISI QUANTITATIVA
  - Misurazioni incoerenti --> La variabilità nella colorazione può portare a misurazioni incoerenti, influenzando l'affidabilità delle analisi quantitative
  - Analisi automatizzate --> Gli algoritmi di analisi automatizzata di immagini fanno affidamento su data input coerenti. Le variazioni nella colorazione possono dare come risultato degli output non accurati o non affidabili
  - Studi comparativi --> Confrontare campioni di tessuto da diverse sorgenti diventa difficile se la colorazione non è coerente, riducendo la validità degli studi comparativi
### 3. RIPRODUCIBILITA' E AFFIDABILITA'
  - Riproducibilità --> Assicurare riproducibilità di risultati su tutte le slide e su tutti gli studi è cruciale per la ricerca scientifica
  - Accuratezza diagnostica --> Nelle impostazioni cliniche, la coerenza può portare a interpretazioni errate delle caratteristiche istologiche

## IL METODO MACENKO COME SUPERA QUESTE SFIDE?

Il metodo Macenko affronta queste sfide fornendo un approccio sistematico per normalizzare le variazioni di colore nelle slide istologiche. Ecco come colma le necessità di coerenza e affidabilità:
### 1. STANDARDIZZAZIONE DELLA COLORAZIONE
  - Normalizzando la distribuzione del colore nelle slide con uno standard di riferimento, assicura coerenza nella colorazione su tutte le slide, su tutti i laboratori e gli studi
### 2. ANALISI QUANTITATIVA AVANZATA
  - Le slide normalizzate forniscono un input coerente per analisi quantitative, migliorando l'accuratezza e l'affidabilità delle misurazioni
  - Gli algoritmi di analisi delle immagini automatizzata lavorano meglio con dati standardizzati, portando ad output più affidabili
### 3. COMPARABILITA' MIGLIORATA
  - La normalizzazione permette confronti significativi tra campioni di tessuti provenienti da diverse sorgenti, aumentando la validità degli studi comparativi
### 4. RIPRODUCIBILITA' AUMENTATA
  - Standardizzare il processo di colorazione migliora la riproducibilità dei risultati, una pietra angolare della ricerca scientifica
  - La colorazione coerente supporta diagnosi accurate e affidabili nelle impostazioni cliniche

## COME FUNZIONA IL METODO MACENKO?

Il metodo Macenko è una tecnica ampiamente usata per la normalizzazione di colori nelle slide istologiche, in particolare per le slide H&E. Esso implica diversi step per trasformare un'immagine in uno spazio normalizzato, riducendo variabilità e migliorando la coerenza per l'analisi quantitativa.

*Spiegazione step-by-step:*
### 1°PASSO. CONVERSIONE DELL'IMMAGINE IN UNO SPAZIO OD
  - Il primo step per convertire un'immagine RGB in uno spazio OD. Questa trasformazione è basata sulla legge di Beer-Lambert, la quale afferma che l'assorbimento della luce che passa attraverso un materiale è proporzionale alla sua concentrazione
  - La formula di conversione è $OD=-log(I/Io)$ , con *I* l'intensità dei pixel nell'immagine e *Io* l'intensità della luce di riferimento (normalmente 255 per un'immagine a 8 bit)
### 2°PASSO. MATRICE PER LA STIMA DELLE MACCHIE
  - Questo metodo usa la Decomposizione dei Valori Singoli(SVD) per trovare le componenti del colore principale nello spazio OD   $OD_{matrix}=U {\Sigma} V^{T}$
  - Ed estrae i primi due vettori singolari da V per formare la matrice delle macchie S --> $S = [V_{1} \space V_{2} ]$
### 3°PASSO. MACCHIE SEPARATE
  - Usa i vettori per separare l'immagine nelle sue componenti. Questo comporta la proiezione dei valori OD nei vettori delle macchie
  - Visto che i valori OD sono proiettati, separano l'immagine in diversi canali di colorazione
### 4°PASSO. NORMALIZZAZIONE DELLE MACCHIE
  - Si normalizzano le componenti delle macchie scalandole per farle combaciare con delle distribuzioni di riferimento. Questo step porta l'intensità delle macchie a uno standard coerente,riducendo la variabilità tra slide
  - Questo comporta la scalatura delle componenti come, per esempio, le loro proprietà statistiche , per farle combaciare con una slide di riferimento
  - Si aggiustano le componenti per farle combaciare con una distribuzione bersaglio, tipicamente derivata da un'immagine di riferimento
$C_{\text{normalized}} = \frac{C - \mu_C}{\sigma_C} \times \sigma_T + \mu_T$ , con *μ_{c}* e *sigma_{c}* rispettivamente la deviazione media e standard delle concentrazioni correnti, mentre *mu_{t}* e *sigma_{t}* la deviazione media e standard delle concentrazioni standard


 









