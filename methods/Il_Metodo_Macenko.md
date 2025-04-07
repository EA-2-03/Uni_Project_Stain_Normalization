Link della fonte delle informazioni:
[https://www.geeksforgeeks.org/macenko-method-for-normalizing-histology-slides-for-quantitative-analysis/]

## COSA E’ IL METODO MACENKO

L’idea principale dietro il metodo Macenko è quella di trasformare un’immagine in uno spazio in Densità Ottica (OD), stimare i vettori delle macchie primarie usando la Decomposizione di Valori Singoli (SVD), separare l’immagine in base alle componenti delle macchie, normalizzare queste componenti in una distribuzione di riferimento, e poi ricostruire l’immagine normalizzata. Questo processo standardizza la distribuzione dei colori in slide delle macchie, facendo analisi successive più coerenti e affidabili. Nella ricerca e diagnosi medica , i colori delle immagini dei tessuti delle macchie devono essere coerenti. Diversi laboratori e procedure possono produrre immagini con colori variabili, facendo diventare così le analisi accurate più difficili da realizzare. Il metodo Macenko standardizza questi colori, assicurando coerenza in tutte le immagini. Questo processo, chiamato normalizzazione delle macchie, aiuta sia i patologi umani che i tools automatizzati nel fare valutazioni più accurate, e crea risultati più affidabili nelle ricerche e diagnosi mediche. 

# QUALI SONO LE SFIDE NEL PROCESSO DI COLORAZIONE DELLE SLIDE DI NORMALIZZAZIONE?

Diverse sfide devono essere superate a causa della grande variabilità nel processo di colorazione:
## 1. VARIABILITA' DELLA COLORAZIONE
  - Differenze di protocollo --> Diversi laboratori possono usare protocolli diversi, portando a differenza in termini di intensità di colorazione e tonalità
  - Lotti di reagenti --> La variabilità tra lotti di reagenti può influire sul colore delle macchie e sulla sua intensità 
  - Preparazione delle slide --> Le differenze nelle tecniche di preparazione delle slide possono introdurre incoerenza nella colorazione
## 2. IMPATTO NELL'ANALISI QUANTITATIVA
  - Misurazioni incoerenti --> La variabilità nella colorazione può portare a misurazioni incoerenti, influenzando l'affidabilità delle analisi quantitative
  - Analisi automatizzate --> Gli algoritmi di analisi automatizzata di immagini fanno affidamento su data input coerenti. Le variazioni nella colorazione possono dare come risultato degli output non accurati o non affidabili
  - Studi comparativi --> Confrontare campioni di tessuto da diverse sorgenti diventa difficile se la colorazione non è coerente, riducendo la validità degli studi comparativi
