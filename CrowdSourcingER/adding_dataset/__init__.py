from .datasets_class import *
import config

def parse_datsets(spark):
    list_rdd_of_datasets = []
    for dataset in config.ADD_DATASETS:
        dataset_class = getattr(datasets_class,dataset["name"].capitalize())
        inst = dataset_class(dataset["path"],spark)
        json_files,entities = inst.parse()
        list_rdd_of_datasets.append((json_files,entities,dataset["vertical"]))
    return list_rdd_of_datasets
