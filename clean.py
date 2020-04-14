import yaml

with open('api.yaml') as f:
    doc = yaml.safe_load(f)

    doc['externalDocs']['url'] = 'https://github.com/jexia/'
    doc['externalDocs']['description'] = 'Management contracts for Jexia Platform'
    doc['info']['title'] = 'Jexia Management Swagger Contracts'
    doc['servers']=[{'description':'Production server','url':'https://app.jexia.com'}]
    doc['paths'].pop('/signup', None)
    doc['tags']=[]
    with open('api.yaml', 'w') as f:
        yaml.safe_dump(doc, f)