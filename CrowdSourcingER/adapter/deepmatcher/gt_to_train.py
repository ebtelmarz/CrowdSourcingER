from itertools import product
import json
import os
from pyspark.sql.functions import col
from pyspark.sql.functions import monotonically_increasing_id
from adapter import utils as u

#A partire dai DataFrame di entities e json_files si creano:

    #-le coppie di istanze positive

    #-le coppie negative facendo il prodotto cartesiano tra gli elementi di instances
    #di diverse entità

    #si effettua l'unione delle coppie e l'aggiunta del page_title per le singole
    #istanze

    #ritorna un DataFrame pandas per effettuare il training
#
def to_train (gt,spark):
    entities,json_files = gt
    positives = entities.rdd.flatMap(lambda e:
                    list(filter(lambda x: x[0]!=x[1],list(product(e.instances,repeat=2)))))\
                    .map(lambda pair:pair+(1,))


    entities_rdd= entities.rdd.map(lambda e : (e.resource_id,e.instances))
    negatives = entities_rdd.cartesian(entities_rdd)\
                        .filter(lambda pair: pair[0][0]!=pair[1][0])\
                        .flatMap(lambda entities_pair:\
                        list(product(entities_pair[0][1],entities_pair[1][1])))\
                        .map(lambda pair:pair+(0,))\

    attributes = json_files.rdd.map(lambda json:\
                        u.take_page_title((json.resource_id,json.source_name,json.json_number)))\
                        .toDF().selectExpr("_1 as resource_id", "_2 as page_title")

    df = positives.union(negatives).toDF()\
            .selectExpr("_1 as ltable_id", "_2 as rtable_id","_3 as label")

    joined = df.join(attributes,df["ltable_id"]==attributes["resource_id"])\
                .select([col(xx) for xx in df.columns]\
                        +[col("page_title").alias("ltable_page_title")])

    joined = joined.join(attributes,joined["rtable_id"]==attributes["resource_id"])\
                    .select([col(xx) for xx in joined.columns]\
                            +[col("page_title").alias("rtable_page_title")])\
                    #.withColumn("_id",monotonically_increasing_id())

    return joined.toPandas()
