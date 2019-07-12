from adapter import utils as u
import os
import config

#-si creano i candidati sottrando a tutti i json_files quelli
#   presenti in instances.
#
#-si prendono i rappresentanti di ogni cluster
#
#-si fa il prodotto cartesiano tra candidati e rappresentati per ottenere
#le coppie su cui effettuare le predizioni
#
#-salva in un csv il dataframe su cui effettuare le predizioni
def to_predict(gt,spark):
    entities,json_files = gt
    instances = entities.rdd.flatMap(lambda e: e.instances).map(lambda e: (e,""))
    json_files = json_files.rdd.map(lambda json:(json.resource_id,(json.source_name,json.json_number)))
    candidates = json_files.subtractByKey(instances)\
                .map(lambda x: u.take_page_title((x[0],x[1][0],x[1][1])))

    repre = take_gt_representative(entities)\
            .join(json_files)\
            .map(lambda x:(x[0],x[1][1][0],x[1][1][1]))\
            .map(lambda x: u.take_page_title((x[0],x[1],x[2])))

    unlabeled = candidates.cartesian(repre)\
            .map(lambda x:(x[0][0],x[1][0],x[0][1],x[1][1]))

    unlabeled.toDF()\
    .selectExpr("_1 as ltable_id", "_2 as rtable_id",\
                "_3 as ltable_page_title","_4 as rtable_page_title")\
    .toPandas()\
    .to_csv(config.PATHS["deepmatcher_unlabeled"],",",index_label="_id")


#da fare una funzione per calcolare il miglior rappresentate del cluster
def take_gt_representative(entities):
    return entities.rdd.map(lambda json: (json.instances[0],""))
