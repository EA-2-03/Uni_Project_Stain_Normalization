Link della fonte delle informazioni:
[https://www.researchgate.net/publication/220518215_Color_Transfer_between_Images] {RICERCA DI SETTEMBRE 2001}

## INTRODUZIONE

In uno spazio RGB, molti pixel devono avere valori ampi per i canali rosso e verde se il canale blu è grande. Questo implica che se si vuole cambiare l'aspetto del colore di un pixel in modo coerente, bisogna modificare tutti i canali insieme. Questo complica ogni processo di modifica del colore. Per fare questo ci serve uno spazio di colore ortogonale senza correlazioni tra gli assi. 
Qualche anno prima della ricerca di Reinhard, Ruderman sviluppa uno spazio chiamato $l \alpha \beta$ ("lab") , il quale minimizza la correlazione tra i canali. Questo spazio è basato sulla ricerca sulla percezione umana basata sui dati che presuppone che il sistema visivo umano sia idealmente adatto per le scene naturali di elaborazione. Gli autori hanno scoperto lo spazio $l \alpha \beta$ nel contesto di scoprire il sistema visivo umano. 
Esiste una piccola correlazione tra gli assi dello spazio $l \alpha \beta$ , perciò bisogna applicare diverse operazioni nei diversi canali . Inoltre, questo spazio è logaritmico, il quale porta a una prima approssimazione che i cambi uniformi di intensità nel canale tendono a essere equamente rilevabili.

## SPAZIO DI COLORE DECORRELATO

L' asse $l$ rappresenta un canale acromatico, mentre i canali $\alpha$ e $\beta$ sono canali cromatici opposti giallo-blu e rosso-verde . I dati di questo spazio sono simmetrici e compatti. 

## STATISTICHE E COLOR CORRECTION

L'obiettivo del lavoro di Reinhard era creare un'immagine sintetica prendendo come riferimento l'aspetto di un'altra immagine. Più formalmente questo vuol dire trasferire dei dati in uno spazio $l \alpha \beta$ tra le immagini. 
Visto che il lavoro di Reinhard assume che si debba trasferire l'aspetto di un'immagine in un'altra, è possibile selezionare le immagini sorgente e target che non lavorano bene insieme. La qualità del risultato dipende dalla somiglianza in composizione tra le immagini. Per esempio, se l'immagine sintetica contiene erba, mentre l'immagine target ha il cielo, si presuppone che lo scambio fallisca.
Si può rimediare facilmente a questo problema. In primo luogo, in questo esempio, si possono selezionare campioni di erba e cielo e calcolare le loro statistiche, avendo così due coppie di cluster in spazio $l \alpha \beta$. Poi, si converte l'intero rendering in uno spazio $l \alpha \beta$  . Da cui si scala ogni pixel nell' immagine di ingresso secondo le statistiche associate con ognuna delle coppie di cluster. Poi, si calcola la distanza dal centro di ogni cluster sorgente e si divide per la deviazione standard del cluster. Questa divisione è richiesta per compensare le diverse dimensioni dei cluster. Si uniscono i pixel scalati con pesi inversamente proporzionali alle distanze normalizzate, producendo il colore finale. Questo approccio si può naturalmente estendere a immagini con più di due cluster. 

## RISULTATI

L'immagine sintetica e l'immagine target hanno composizioni simili, rendendo possibile il trasferimento dell'aspetto dell'immagine target sull'immagine sintetica.
Con questo metodo viene mostrato che lo spazio $l \alpha \beta$ si può usare per la correzione della tonalità usando l'ipotesi del mondo grigio.

## CONCLUSIONI

Questo metodo dimostra che uno spazio di colore con assi non correlati è uno strumento utile per manipolare il colore delle immagini. Imporre la deviazione media e la deviazione standard nei dati è una semplice operazione, la quale produce immagini di output credibili date immagini di input adatte. La semplicità di questo metodo consente di implementarlo come plug-in in vari pacchetti di grafica commerciali. 
