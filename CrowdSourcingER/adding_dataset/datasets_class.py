from pyspark.sql import SparkSession
from .wrappers import *

class Anhai:
    def __init__(self,path,spark):
        super().__init__()
        self.__path=path
        self.__spark =spark

    def parse(self):
        spark = self.__spark

        #creazione rdd da file
        dataset = spark.read.option("quote","\"")\
                    .option("delimiter",",")\
                    .csv(self.__path)\
                    .rdd\
                    .map(lambda line: tuple([x for x in line]))

        json_entity_rdd = dataset.flatMap(lambda line:anhai_json(line))

        return (json_entity_rdd.filter(lambda json: json['resource_class']=='json_file'),\
                json_entity_rdd.filter(lambda json: json['resource_class']=='entity'))

#create the json_file and the entity_class for a line of dataset
def anhai_json(line):
    json1 ={
                'id': line[1],
                'director': line[3],
                'name':line[4],
                'date':line[5]
            }

    json2 = {
                'id': line[2],
                'director': line[6],
                'name':line[7],
                'date':line[8]
            }


    return [wrap_json_file(json1),wrap_json_file(json2),wrap_entity_class(json1,json2)]
