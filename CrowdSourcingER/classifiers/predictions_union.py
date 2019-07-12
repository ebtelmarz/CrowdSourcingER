from storing import mongoDB as md
import pyspark.sql.functions as f

#prende in input una lista di Dataframe con le predizioni
def union(spark,fpairs,dm,m,jd):
    union = dm.rdd.union(m.rdd).union(jd.rdd)\
                .map(lambda row:((row.ltable_id,row.rtable_id)\
                                ,(row.match_score\
                                ,row.ltable_page_title\
                                ,row.rtable_page_title)))\
                .reduceByKey(lambda a,b:a +(b[0],b[1],b[2]))\
                .map(lambda row:(row[0][0],row[0][1],row[1][1],row[1][2]\
                                 ,row[1][0],row[1][3],row[1][6]))

    if(not(fpairs.rdd.isEmpty())):
        rdd_pair = fpairs.rdd.map(lambda row:(row.left+row.right,"")).toDF()\
                        .selectExpr("_1 as pair_id", "_2 as vuoto")

        union_df = union.map(lambda row:(row[0]+row[1],row))\
                                .toDF()\
                                .selectExpr("_1 as id", "_2 as row")

        union_filtered = union_df.join(rdd_pair,union_df["id"]==rdd_pair["pair_id"],"leftouter")\
                                .filter(f.isnull("pair_id"))\
                                .drop(f.col("vuoto"))\
                                .drop(f.col("pair_id"))\



        return union_filtered.rdd.map(lambda row:row.row)\
                            .toDF()\
                            .selectExpr("_1 as ltable_id", "_2 as rtable_id",\
                                        "_3 as ltable_page_title","_4 as rtable_page_title",\
                                        "_5 as deepmatcher_score","_6 as magellan_score",\
                                        "_7 as jedai_score")\
                            .toPandas()
    else:
        return union.toDF()\
            .selectExpr("_1 as ltable_id", "_2 as rtable_id",\
                        "_3 as ltable_page_title","_4 as rtable_page_title",\
                        "_5 as deepmatcher_score","_6 as magellan_score",\
                        "_7 as jedai_score")\
            .toPandas()
