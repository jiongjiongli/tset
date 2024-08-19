import re
import json
import random
import numpy as np


def variable_replace(query):
    newvars = ['?vr0','?vr1','?vr2','?vr3','?vr4','?vr5']
    variables = set([x for x in query.split() if x[0] == '?'])
    for idx,var in enumerate(sorted(variables)):
        if var == '?maskvar1': continue
        query = query.replace(var,newvars[idx])
    return query.lower()

def flip_tuple(query):
    query = variable_replace(query)
    query_flip = query

    string = query[query.find('{')+1:query.find('}')]
    if 'filter' in string:
        string = string[:string.find('filter')]
    tuples = string.strip(' .').strip().split('.')

    for item in tuples:
        item = item.strip()
        item_list = item.split()
        item_list = np.random.permutation(item_list)
        query_flip = query_flip.replace(item, ' '.join(item_list))

    return query, query_flip

input_dir_path = './lc_quad_pre_cn'
output_dir_path = './lc_quad_pre_cn'

train = json.load(open(f'{input_dir_path}/sparql_cn_train.json','rb'))
test = json.load(open(f'{input_dir_path}/sparql_cn_test.json', 'rb'))
sparql_test = [item['sparql_wikidata'] for item in test]
sparql_train = [item['sparql_wikidata'] for item in train]


datas_test = []
for item in sparql_test:
    target,inputs = flip_tuple(item)
    datas_test.append({'input':inputs, 'target':target})

datas_train = []
for item in sparql_train:
    target,inputs = flip_tuple(item)
    datas_train.append({'input':inputs, 'target':target})


dict_json_test=json.dumps(datas_test, indent=2)

with open(f'{output_dir_path}/flip_test.json','w') as file:
    file.write(dict_json_test)

dict_json_train=json.dumps(datas_train, indent=2)

with open(f'{output_dir_path}/flip_train.json','w') as file:
    file.write(dict_json_train)
