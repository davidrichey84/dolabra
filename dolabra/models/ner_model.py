import sys
class NERModel():
    def __init__(self):
        model = '/Users/davidrichey/Documents/dev/dolabra/utilities/output/shitbox'
        try:
            self.ner_model = spacy.load(model)
        except Exeption as e:
            print("Could not locate model!")
            print(str(e))
            sys.exit(1)

    def classify(self, message):
        classify_log = self.ner_model(message)
        payload = {'results': []}
        for item in classify_log.ents:
            payload['results'].append({item.label_: item.text})
        return payload