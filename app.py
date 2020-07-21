import ujson
import falcon
import spacy
import sys

class Classify(object):
    def __init__(self):
        model = 'utilities/syslog_ner.model'
        try:
            self.ner_model = spacy.load(model)
        except:
            print("Could not locate model!")
            sys.exit(1)

    def on_get(self, req, resp):
        payload = req.media
        try:
            classify_log = ''
            if 'data' in payload:
                classify_log = self.ner_model(payload['data'])
                if classify_log and len(classify_log) > 1:
                    payload = {'results':[]}
                    for item in classify_log.ents:
                        payload['results'].append({item.label_: item.text})
                    resp.body = ujson.dumps(payload)
                    resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_404
        except Exception as e:
            resp.body = str(e)
            resp.status = falcon.HTTP_500

app = falcon.API()
classification = Classify()
app.add_route('/api/classify', classification)