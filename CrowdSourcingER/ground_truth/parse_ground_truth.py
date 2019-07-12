import json
import os
import config

def parse_entites(spark):
    path_entities = config.PATHS["entities_gt"]
    df = spark.read.json(path_entities, multiLine=True)
    return df

def parse_json_files(spark):
    path_entities = config.PATHS["json_files"]
    df = spark.read.json(path_entities, multiLine=True)
    return df
