import json
import os

#a partire da resource_id,source_name,json_numbe ottiene il page_title dell'istanza
def take_page_title(pair):
    resource_id,source_name,json_number = pair
    f = json.load(open(os.path.join(".","2013_camera_dataset",source_name,str(json_number)+".json")))
    return (resource_id,f["<page title>"])
