import yaml

with open('api.yaml') as f:
    doc = yaml.safe_load(f)

    doc['externalDocs']['url'] = 'https://github.com/jexia/'
    doc['externalDocs']['description'] = 'Management contracts for Jexia Platform'
    doc['info']['title'] = 'Jexia Management Swagger Contracts'
    doc['servers']=[{'description':'Production server','url':'https://app.jexia.com'},{'url': 'https://services.jexia.com/management/{project_id}','description': 'Service endpoint for all paths below'}]
    doc['paths'].pop('/signup', None)
    doc['tags']=[]
#================= Adjust DataSet contracts ====================    
    name = ['paths for Dataset']
    doc['paths']['/ds/']['get']['tags']=name 
    doc['paths']['/ds/']['post']['tags']=name
    doc['paths']['/ds/{dataset_id}']['put']['tags']=name
    doc['paths']['/ds/{dataset_id}']['delete']['tags']=name
    doc['paths']['/ds/{dataset_id}/data']['delete']['tags']=name
    doc['paths']['/ds/{dataset_id}/field']['post']['tags']=name
    doc['paths']['/ds/{dataset_id}/field/{field_id}']['put']['tags']=name
    doc['paths']['/ds/{dataset_id}/field/{field_id}']['delete']['tags']=name
    doc['paths']['/ds/{dataset_id}/constraint/{field_id}']['post']['tags']=name
    doc['paths']['/ds/{dataset_id}/constraint/{constraint_id}']['put']['tags']=name
    doc['paths']['/ds/{dataset_id}/constraint/{constraint_id}']['delete']['tags']=name
    doc['paths']['/ds/{dataset_id}/constraints/{field_id}']['put']['tags']=name
    doc['paths']['/ds/relation']['post']['tags']=name
    doc['paths']['/ds/relation/{relation_id}']['delete']['tags']=name
    
    doc['paths']['/mimir/ds/']=doc['paths']['/ds/']
    del doc['paths']['/ds/']
    
    doc['paths']['/mimir/ds/{dataset_id}']=doc['paths']['/ds/{dataset_id}']
    del doc['paths']['/ds/{dataset_id}']
    
    doc['paths']['/mimir/ds/{dataset_id}/data']=doc['paths']['/ds/{dataset_id}/data']
    del doc['paths']['/ds/{dataset_id}/data']
    
    doc['paths']['/mimir/ds/{dataset_id}/field']=doc['paths']['/ds/{dataset_id}/field']
    del doc['paths']['/ds/{dataset_id}/field']
    
    doc['paths']['/mimir/ds/{dataset_id}/constraint/{field_id}']=doc['paths']['/ds/{dataset_id}/constraint/{field_id}']
    del doc['paths']['/ds/{dataset_id}/constraint/{field_id}']
    
    doc['paths']['/mimir/ds/relation']=doc['paths']['/ds/relation']
    del doc['paths']['/ds/relation']
    
    doc['paths']['/mimir/ds/relation/{relation_id}']=doc['paths']['/ds/relation/{relation_id}']
    del doc['paths']['/ds/relation/{relation_id}']
    
    doc['paths']['/mimir/ds/{dataset_id}/constraint/{constraint_id}']=doc['paths']['/ds/{dataset_id}/constraint/{constraint_id}']
    del doc['paths']['/ds/{dataset_id}/constraint/{constraint_id}']
    
    doc['paths']['/mimir/ds/{dataset_id}/constraints/{field_id}']=doc['paths']['/ds/{dataset_id}/constraints/{field_id}']
    del doc['paths']['/ds/{dataset_id}/constraints/{field_id}']
    
    doc['paths']['/mimir/ds/{dataset_id}/field/{field_id}']=doc['paths']['/ds/{dataset_id}/field/{field_id}']
    del doc['paths']['/ds/{dataset_id}/field/{field_id}']

#=================== Adjust FileSet ================
    name = ['paths for FileSet']
    doc['paths']['/fs/']['get']['tags']=name 
    doc['paths']['/storage/']['post']['tags']=name 
    doc['paths']['/fs/']['post']['tags']=name
    doc['paths']['/fs/{fileset_id}']['put']['tags']=name
    doc['paths']['/fs/{fileset_id}']['delete']['tags']=name
    doc['paths']['/fs/{fileset_id}/field']['post']['tags']=name
    doc['paths']['/fs/{fileset_id}/field/{field_id}']['put']['tags']=name
    doc['paths']['/fs/{fileset_id}/field/{field_id}']['delete']['tags']=name
    doc['paths']['/fs/{fileset_id}/constraint/{field_id}']['post']['tags']=name
    doc['paths']['/fs/{fileset_id}/constraint/{constraint_id}']['put']['tags']=name
    doc['paths']['/fs/{fileset_id}/constraint/{constraint_id}']['delete']['tags']=name
    doc['paths']['/fs/{fileset_id}/constraints/{field_id}']['put']['tags']=name
    doc['paths']['/fs/relation']['post']['tags']=name
    doc['paths']['/fs/relation/{relation_id}']['delete']['tags']=name

    doc['paths']['/bestla/storage/']=doc['paths']['/storage/']
    del doc['paths']['/storage/']
    
    doc['paths']['/bestla/fs/']=doc['paths']['/fs/']
    del doc['paths']['/fs/']

    doc['paths']['/bestla/fs/{fileset_id}']=doc['paths']['/fs/{fileset_id}']
    del doc['paths']['/fs/{fileset_id}']
    
    doc['paths']['/bestla/fs/{fileset_id}/field']=doc['paths']['/fs/{fileset_id}/field']
    del doc['paths']['/fs/{fileset_id}/field']
    
    doc['paths']['/bestla/fs/{fileset_id}/constraint/{field_id}']=doc['paths']['/fs/{fileset_id}/constraint/{field_id}']
    del doc['paths']['/fs/{fileset_id}/constraint/{field_id}']
    
    doc['paths']['/bestla/fs/relation']=doc['paths']['/fs/relation']
    del doc['paths']['/fs/relation']
    
    doc['paths']['/bestla/fs/relation/{relation_id}']=doc['paths']['/fs/relation/{relation_id}']
    del doc['paths']['/fs/relation/{relation_id}']
    
    doc['paths']['/bestla/fs/{fileset_id}/constraint/{constraint_id}']=doc['paths']['/fs/{fileset_id}/constraint/{constraint_id}']
    del doc['paths']['/fs/{fileset_id}/constraint/{constraint_id}']
    
    doc['paths']['/bestla/fs/{fileset_id}/constraints/{field_id}']=doc['paths']['/fs/{fileset_id}/constraints/{field_id}']
    del doc['paths']['/fs/{fileset_id}/constraints/{field_id}']
    
    doc['paths']['/bestla/fs/{fileset_id}/field/{field_id}']=doc['paths']['/fs/{fileset_id}/field/{field_id}']
    del doc['paths']['/fs/{fileset_id}/field/{field_id}']

    with open('api.yaml', 'w') as f:
        yaml.safe_dump(doc, f)