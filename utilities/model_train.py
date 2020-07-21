import yaml
import json
import spacy
import random
from tqdm import tqdm


def read_yaml(yaml_file):
    with open("syslog1.yaml") as yaml_in:
        yaml_object = yaml.safe_load(yaml_in)
        return yaml_object

def create_training_set(json_training_data):
    training_data = []
    for item in json_training_data['training_set']:
        temp_list = []
        temp_list.append(item['training_log']['log'])
        #temp_list.append({'entities': []})
        entities = {'entities': []}
        for entity in item['training_log']['entities']:
            entities['entities'].append((entity['start'], entity['end'], entity['label']))
        temp_list.append(entities)
        training_data.append(tuple(temp_list))
    print(training_data)
    return training_data

def add_ner_pipe_to_model(ner_model, training_data):
    if 'ner' not in ner_model.pipe_names:
        ner_pipe = ner_model.create_pipe('ner')
        ner_model.add_pipe(ner_pipe, last=True)

        for _, annotations in training_data:
            for ent in annotations.get('entities'):
                ner_pipe.add_label(ent[2])
        return ner_pipe, ner_model

def train_model(ner_model, training_data):
    other_pipes = [pipe for pipe in ner_model.pipe_names if pipe != 'ner']
    with ner_model.disable_pipes(*other_pipes):
        optimizer = ner_model.begin_training()
        for itn in range(100):
            random.shuffle(training_data)
            losses = {}
            for text, annotations in tqdm(training_data):
                ner_model.update(
                            [text],
                            [annotations],
                            drop=0.5,
                            sgd=optimizer,
                            losses=losses)
            print(losses)
    return ner_model

if __name__ == "__main__":
    ner_model = spacy.blank('en')
    print("Created new blank model")
    json_training_data = read_yaml('syslog1.yaml')
    training_data = create_training_set(json_training_data)
    ner_pipe, ner_updated_model = add_ner_pipe_to_model(ner_model, training_data)
    ner_final_model = train_model(ner_updated_model, training_data)
    print("All done!\n")
    for text, _ in training_data:
        doc = ner_final_model('May 14 05:47:20 tor01.r1.dal PortSec: %ETH-4-HOST_FLAPPING: Host ff:00:ff:00:ff:00 in VLAN 1900 is flapping between interface Port-Channel555 and interface Ethernet37 (message repeated 23 times in 5.51062 secs)')
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])

    ner_final_model.to_disk('syslog_ner.model')






