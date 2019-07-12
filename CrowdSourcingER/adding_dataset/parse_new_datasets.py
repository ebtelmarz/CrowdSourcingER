from storing import mongoDB as mDB
import parsing_dataset as pd
import config
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('bigData').getOrCreate()

#parse all datasets
list_parsed_datasets = pd.parse_datsets(spark)

#se ci sono nuovi dataset da aggiungere
if len(list_parsed_datasets)>0:
    #storing json_files and entity_class
    mDB.store_datasets(list_parsed_datasets)
    config.DATASETS = config.DATASETS + config.ADD_DATASETS
    config.ADD_DATASETS = []
