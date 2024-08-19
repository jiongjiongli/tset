import os
from pathlib import Path
import re
import json
from tqdm import tqdm


vocab = ['"', '(', 'rdfs:label', 'by', 'ask', '>', 'select', 'que', 'limit', 'jai', 'mai',
                 '?sbj', ')', 'lang', 'year', '}', '?value', 'peint', 'desc', 'where', 'ce',
                 'distinct',  'filter', 'lcase', 'order', 'la', '<', 'asc', 'en', 'contains',
                 'as', ',', 'strstarts',  '{', "'", 'j', 'count', '=', '.', '?vr0', '?vr1',
                 '?vr2', '?vr3', '?vr4', '?vr5', '?vr6',  '?vr0_label', '?vr1_label', '?vr2_label',
                 '?vr3_label', '?vr4_label', '?vr5_label', '?vr6_label', 'wd:', 'wdt:', 'ps:',
                 'p:', 'pq:', '?maskvar1', '[DEF]','[Entity]', '[Relation]', 'null']

dict_vocab={}
for i,text in enumerate(vocab):
    dict_vocab['<extra_id_'+str(i+30)+'>']=text


class Preprocess(object):
    def __init__(self):

        ent_labels = json.load(open(f'{input_dir_path}/entity.json', 'rb'))
        rel_labels = json.load(open(f'{input_dir_path}/relation.json', 'rb'))

        vocab = ['"', '(', 'rdfs:label', 'by', 'ask', '>', 'select', 'que', 'limit', 'jai', 'mai',
                 '?sbj', ')', 'lang', 'year', '}', '?value', 'peint', 'desc', 'where', 'ce',
                 'distinct',  'filter', 'lcase', 'order', 'la', '<', 'asc', 'en', 'contains',
                 'as', ',', 'strstarts',  '{', "'", 'j', 'count', '=', '.', '?vr0', '?vr1',
                 '?vr2', '?vr3', '?vr4', '?vr5', '?vr6',  '?vr0_label', '?vr1_label', '?vr2_label',
                 '?vr3_label', '?vr4_label', '?vr5_label', '?vr6_label', 'wd:', 'wdt:', 'ps:',
                 'p:', 'pq:', '?maskvar1', '[DEF]','[Entity]', '[Relation]', 'null']

        vocab_dict={}
        for i,text in enumerate(vocab):
            vocab_dict[text]='<extra_id_'+str(i+30)+'>'

        for kk in ent_labels:
            if ent_labels[kk] is None: ent_labels[kk] = vocab_dict['null']

        self.ent_labels = ent_labels
        self.rel_labels = rel_labels
        self.vocab_dict = vocab_dict


    def process(self, wikisparql):
        sparql = wikisparql.replace('(',' ( ').replace(')',' ) ').replace('{',' { ')\
        .replace('}',' } ').replace(':',': ').replace(',',' , ').replace("'"," ' ")\
        .replace('.',' . ').replace('=',' = ').lower()
        sparql = ' '.join(sparql.split())

        split = sparql.split()
        for idx, item in enumerate(split):
            if item in self.ent_labels:
                split[idx] = self.ent_labels[item]
            elif item in self.rel_labels:
                split[idx] = self.rel_labels[item]

            if item in self.vocab_dict:
                split[idx] = self.vocab_dict[item]

        return ' '.join(split).strip()

    def _preprocess(self, data):
        # res = {'input': self.process(data['input']), 'target': self.process(data['target'])}

        return {'input': self.process(data['input']), 'target': self.process(data['target'])}


input_dir_path = './lc_quad_pre_cn'
output_dir_path = './transform/transformers_cache/downloads/LC-QuAD_CN/dataset'
Path(output_dir_path).mkdir(parents=True, exist_ok=True)

test_data = json.load(open(f'{input_dir_path}/flip_test.json', 'rb'))
train_data = json.load(open(f'{input_dir_path}/flip_train.json', 'rb'))


pre = Preprocess()

train = [pre._preprocess(item) for item in tqdm(train_data)]

with open(f'{output_dir_path}/train.json','w') as file:
    file.write(json.dumps(train, indent=2))


test = [pre._preprocess(item) for item in tqdm(test_data)]

with open(f'{output_dir_path}/test.json','w') as file:
    file.write(json.dumps(test, indent=2))
