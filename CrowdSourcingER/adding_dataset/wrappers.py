def wrap_json_file(json):
    return {
        'resource_class' : 'json_file',
        #"resource_id": "JSON#1",
        #"source_id": "SOURCE#1"
        'value' : json
    }

def wrap_entity_class(json1,json2):
    return {
        'resource_class' : 'entity',
        'instances':[
            json1,
            json2
        ]
    }
