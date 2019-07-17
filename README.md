# CrowdSourcingER

Implementazione di una pipeline iterativa con lo scopo di espandare la ground truth di un dataset di fotocamere
riconoscendo quali istanze del dataset rappresentano la stessa entità del mondo reale.

## Pre-requisiti

- Python 3.6
- Spark(consigliato 2.3.3)
- MongoDB(consigliato 4.0.10)
- pymongo
- pymongo_spark
- py_entitymatching
- deepmatcher

## Quick-start

* Connettersi al demone di MongoDB tramite il seguente comando ed inserire la password
```
ssh -N -f -L localhost:8890:localhost:27017 deangelis@enit.inf.uniroma3.it  
```
* Per la prima esecuzione eseguire initialize.sh per creare la ground truth iniziale
* Eseguire start.sh per far partire un ciclo della pipeline iterativa
* Eseguire start_oracolo.sh per aprire una form in cui filtrare le predizioni sbagliate
* Eseguire expand_gt.sh per espandere la ground truth

**Nota bene**
Per poter salvare i risultati dell'oracolo devono essere etichettate tutte le entry



