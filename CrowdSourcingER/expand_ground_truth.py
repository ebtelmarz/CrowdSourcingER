import pandas as pd
import os
from pyspark.sql import SparkSession
from storing import mongoDB as md

df = pd.read_csv(os.path.join(".","oracolo","true_predictions.csv"))

spark = SparkSession.builder.appName('bigData')\
                    .config("spark.mongodb.output.uri","mongodb://localhost:27017/test.MyCollection")\
                    .getOrCreate()

for index,row in df.iterrows():
    if row["response"]==1:
        md.expand_ground_truth(spark,row['ltable_id'],row['rtable_id'],"cameras")
    if row["response"]==0:
        md.expand_ground_false(spark,row['ltable_id'],row['rtable_id'],"cameras")
