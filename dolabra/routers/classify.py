import fastapi
from models.log import LogMessage
import spacy
import sys

router = fastapi.APIRouter()

class NERModel():
    def __init__(self):
        model = '/Users/davidrichey/Documents/dev/dolabra/utilities/output/model-last'
        try:
            self.ner_model = spacy.load(model)
        except:
            print("Could not locate model!")
            sys.exit(1)

    def classify(self, message):
        classify_log = self.ner_model(message)
        payload = {'results': []}
        for item in classify_log.ents:
            payload['results'].append({item.label_: item.text})
        return payload

ner_model = NERModel()

@router.post("/v1/classify")
def classify(payload: LogMessage):
    # do things about classifying the log message
    print(payload)
    print(payload.message)
    classify_log = ner_model.classify(payload.message)
    if classify_log:
        print("entered thid")
        result = []
        for item in classify_log.items():
            #result['results'].append({item.label_: item.text})
            result.append({item[0]: item[1]})
#
        return result
