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

Connettersi alla Tesla tramite il comando
```
ssh nvidia@tesla.inf.uniroma3.it
```
Attivare l'environment di anaconda
```
conda activate testenv
```
Posizionarsi all'interno della cartella del progetto
```
cd workspace/dbgroup/benchmark/CrowdSourcingER
```

## Prima esecuzione

Per la prima esecuzione eseguire
```
sh initialize.sh
```
 
Per verificare la corretta creazione del database contenente la ground truth eseguire
```
python3

from pymongo import MongoClient
c = MongoClient("mongodb://enit.inf.uniroma3.it:8080")
c.list_database_names()
```

## Esecuzione di un ciclo

Controllare lo stato delle GPU
```
nvidia-smi
```
Eseguire un ciclo della pipeline utilizzando le GPU libere specificandone l'id
```
CUDA_VISIBLE_DEVICE = 0,1 sh start.sh
```
Il processo può richiede fino a 20 minuti, dipende dal numero di GPU utilizzate


Le predizioni possono essere trovate all'interno della cartella
```
./classifiers/<blackbox>/prediction_files
```
Un file per ogni blackbox

## Oracolo
Per etichettare le predizioni eseguire il comando
```
sh start_oracolo.sh
```
Verrà avviato un notebook di jupyter con associato un link che apparirà sulla shell.
```
http://localhost:8989/?token=0a8aa13f83e307310006721ad0ffe0b44e90d65465206b37
```
Effettuare un port tunnelling tramite il comando da una nuova shell
```
ssh -N -f -L 8888:localhost:8888 nvidia@tesla.inf.uniroma3.it
```
Andando a sostituire il numero delle porte con quello specificato nel link.

Copiare il link del notebook nel browser ed eseguire il run.
**Nota bene: il file può essere salvato solo se vengono etichettate tutte le coppie di istanze**


