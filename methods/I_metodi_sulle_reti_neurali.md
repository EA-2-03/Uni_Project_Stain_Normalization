Link della fonte delle informazioni: [https://pmc.ncbi.nlm.nih.gov/articles/PMC8602577/] {RICERCA DEL 2021}

# StainNet, un network di normalizzazione veloce e robusto

La normalizzazione convenzionale di solito si ottiene attraverso un modello di mappatura del colore pixel-by-pixel, il quale dipende dall'immagine di riferimento, ed è difficile raggiungere accuratamente la trasformazione dello stile tra i dataset. In principio, questa difficoltà può essere risolta con i metodi basati sul deep-learning, mentre, la sua struttura complicata risulta in bassa efficienza computazionale e artefatti nella trasformazione, la quale restringe l'applicazione pratica. In questo metodo, viene usato il distillation learning (trasferire la conoscenza da modelli grandi a modelli più piccoli) per ridurre la complessità dei metodi di deep-learning e un network veloce e robusto chiamato StainNet per imparare la mappatura del colore tra l'immagine sorgente e l'immagine target. StainNet può imparare la relazione della mappatura da un singolo dataset e aggiusta i valori del colore in maniera pixel-to-pixel. 
La maniera pixel-to-pixel riduce la dimensione del network e evita artefatti nella trasformazione. I risultati sui dataset citopatologici e istopatologici mostrano che StainNet può raggiungere performance paragonabili ai metodi basati sul deep-learning. I risultati del calcolo dimostrano che StainNet è più veloce di 40 volte rispetto a StainGAN e può normalizzare un' immagine WSI 100000x100000 in 40 secondi. 

## INTRODUZIONE

La normalizzazione è una operazione di routine pre-elaborazione per le immagini patologiche, specialmente per sistemi CAD, ed è noto che aiuta il miglioramento dell'accuratezza nella previsione, come la classificazione dei tumori. Gli algoritmi di normalizzazione di solito trasferiscono lo stile del colore dell'immagine sorgente nell'immagine target mentre si preservano le altre informazioni nell'immagine processata, i quali possono essere ampiamente classificati in due classi: metodi convenzionali e metodi basati su deep-learning. 
I metodi convenzionali sono realizzati principalmente analizzando, convertendo e accoppiando le componenti del colore, il quale può essere diviso in metodi di color matching e metodi di separazione delle macchie. I metodi di color matching calcolano la deviazione media e standard delle immagini sorgente e le accoppiano con un immagine di riferimento. I metodi di separazione delle macchie cercano di separare e normalizzare ogni canale di colore indipendentemente. 
I metodi basati su deep-learning impiegano maggiormente le GAN (generative adversial networks, reti generative avverse) per raggiungere la normalizzazione. A causa della complessità delle reti deep neural e l'instabilità delle GAN, è difficile preservare tutte le informazioni della sorgente, e certe volte si corre il rischio di introdurre artefatti, i quali hanno effetti avversi nell'analisi seguente. Allo stesso tempo, la rete dei metodi basati sul deep-learning di solito contengono milioni di parametri, percio' richiede genericamente risorse di calcolo molto alte e l'efficienza di calcolo è genericamente bassa. 
I metodi basati sul deep-learning lavorano bene nella normalizzazione delle macchie, ma non soddisfano in robustezza e efficienza di calcolo. 
Il metodo proposto usa un network chiamato StainNet, il quale attiva una rete di convoluzione 1x1 per aggiustare i valori del colore in maniera pixel-by-pixel. In questo metodo, StainGAN è stato usato come network "maestro" e StainNet come network "studente" per imparare la mappatura del colore tramite il distillation learning.

## ESPERIMENTI E RISULTATI

In questa sezione, StainNet è stato confrontato con i metodi di [Macenko](methods/Il_Metodo_Macenko.md) ,  [Reinhard](methods/Il_Metodo_Reinhard.md) , [Vahadane](methods/Il_Metodo_Vahadane.md) nei dataset citopatologici e istopatologici. 
Vengono riportati:
  - Confronto quantitativo dei diversi metodi nell'aspetto visivo
  - Risultati nella task di classificazione della citopatologia e dell'istopatologia
  - Confronto quantitativo tra i risultati della normalizzazione delle WSI e i risultati del rilevamento della metastasi nelle WSI.

### METRICHE DI VALUTAZIONE

Per valutare le performance dei diversi metodi, è stata misurata la somiglianza tra l'immagine normalizzata e l'immagine target, e la coerenza tra le due immagini. 
Per valutare le performance sono state usate due metriche di somiglianza: il SSIM (indice di somiglianza strutturale) e il PSNR (rateo di picco segnale-rumore). Il SSIM e il PSNR dell'immagine target sono stati usati per valutare la somiglianza tra l'immagine normalizzata e l'immagine target. 
Il SSIM target e il PSNR target sono stati calcolati usando i valori RGB originali. Il SSIM sorgente è stato usato per misurare la conservazione delle informazioni delle texture dell'immagine sorgente, per calcolare il SSIM sorgente è stata usata la scala di grigi. 

### IMPLEMENTAZIONE

Nei metodi convenzionali, quali Macenko, Vahadane e Reinhard, un immagine scelta con cura è stata usata come immagine di riferimento. Per la StainGAN, il modello è stato allenato con Adam optimizer, e l'allenamento è stato fermato alla 100ª epoca. Per StainNet, la StainGAN allenata è stata usata per normalizzare le immagini sorgente sia nel dataset di allenamento che nel dataset di test. Successivamente, le immagini normalizzate sono state usate come verità di base durante l'allenamento. L'allenamento è stato bloccato alla 60ª epoca, la quale è stata scelta sperimentalmente. L'esperimento è stato ripetuto 20 volte per migliorare l'affidabilità. 

## RISULTATI

### RISULTATI NEL TRASFERIMENTO DELLE MACCHIE

In primo luogo, è stata valutata l'efficacia di questo metodo. Le immagini normalizzate da StainNet sono state valutate con le immagini target attraverso la visione e i profili dei valori grigi attorno ai nuclei cellulari. I profili dei valori grigi delle immagini normalizzate da StainNet e le immagini target coincidono nel complesso, indicando che , dopo essere state normalizzate da StainNet, le immagini normalizzate hanno una distribuzione del colore molto simile alle immagini target. 

## DISCUSSIONE E CONCLUSIONE

In questo studio si è raggiunta la normalizzazione usando un network convoluzionale 1x1 in maniera pixel-to-pixel, il quale non solo evita un'efficienza computazionale bassa e possibili artefatti dei metodi basati su deep-learning, ma mantiene le informazioni dell'immagine sorgente. Confrontato con i metodi convenzionali, StainNet impara la relazione nella mappatura in tutto il dataset invece di fare riferimento su una singola immagine, in modo tale da ottenere un'immagine normalizzata con alta somiglianza. 
I risultati mostrano che StainNet ha migliori performance, specialmente per quanto riguarda efficienza computazionale e robustezza.
In poche parole, StainNet è un network di normalizzazione delle macchie veloce e robusto, il quale ha il potenziale di attuare la normalizzazione in tempo reale in un sistema CAD del mondo reale. 
