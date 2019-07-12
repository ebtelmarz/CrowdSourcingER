from itertools import product
from adapter import utils as u
from pyspark.sql.functions import col
import json
import os
import config

def to_train(entities,json_files):
    df = entities.rdd.flatMap(lambda row:\
                                list(filter(lambda x: x[0]!=x[1],\
                                list(product(row.instances,repeat=2)))))\
                .toDF().selectExpr("_1 as ltable_id", "_2 as rtable_id")

    attributes = json_files.rdd.map(lambda row:\
                (row.resource_id,row.source_name,row.json_number))\
                .toDF().selectExpr("_1 as resource_id", "_2 as source_name", "_3 as json_number")

    joined = df.join(attributes,df["ltable_id"]==attributes["resource_id"])\
                .select([col(xx) for xx in df.columns]\
                        +[col("source_name").alias("ltable_source_name")]\
                        +[col("json_number").alias("ltable_json_number")])

    gt_jedai = joined.join(attributes,joined["rtable_id"]==attributes["resource_id"])\
                    .select([col(xx) for xx in joined.columns]\
                            +[col("source_name").alias("rtable_source_name")]\
                            +[col("json_number").alias("rtable_json_number")])\
                    .rdd.map(lambda row: ((row.ltable_source_name+"//"+str(row.ltable_json_number)),\
                                    (row.rtable_source_name+"//"+str(row.rtable_json_number))))
    gt_jedai.toDF()\
        .selectExpr("_1 as instance_left", "_2 as instance_right")\
        .toPandas().to_csv(config.PATHS["jedai_gt"],sep="^",index=False)


    page_titles = json_files.rdd.map(lambda row: \
                            u.take_page_title((row.resource_id,\
                                        row.source_name,\
                                        row.json_number))+(row.json_number,row.source_name))\
                            .map(lambda pair: (pair[3]+"//"+str(pair[2]),pair[1]))\
                            .toDF()\
                            .selectExpr("_1 as url","_2 as page_title")\
                            .toPandas()\
                            .to_csv(config.PATHS["jedai_page_titles"],sep="^",index=False)
