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

* Scaricare il dataset di fotocamere e metterlo all'interno della cartella CrowdSourcingER/2013_camera_dataset/
* Fare lo start di MongoDB
* Per la prima esecuzione eseguire initialize.sh per creare la ground truth iniziale
* Eseguire start.sh per far partire un ciclo della pipeline iterativa
* Eseguire start_oracolo.sh per aprire una form in cui filtrare le predizioni sbagliate
* Eseguire expand_gt.sh per espandere la ground truth

**Nota bene**
Per poter salvare i risultati dell'oracolo devono essere etichettate tutte le entry



