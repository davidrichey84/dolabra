import ujson
import falcon
import spacy
import sys
from argparse import ArgumentParser

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

def setup_arg_parser():
    parser = ArgumentParser()
    parser.add_argument("-k", "--kafka", action='store_true', help="Kafka message queue mode", required=False)
    parser.add_argument("-n", "--nats", action='store_true', help="Nats message queue mode", required=False)
    parser.add_argument("-t", "--target", action='store', dest='target_server', help="Target kafka/NATS server:port", required=False)
    parser.add_argument("-st", "--subtopic", action='store', dest='sub_topic', help="Subscription topic you would like to subscribe to", required=False)
    parser.add_argument("-pt", "--pubtopic", action='store', dest='pub_topic', help="Publish topic you would like to publish results to", required=False)
    parser.add_argument("-r", "--restapi", action='store_true', help="REST API mode", required=False)
    parser.add_argument("-b", "--bind", action='store', dest='bind', help="Interface and port to bind REST API. ex: 0.0.0.0:5000", required=False)
    parder.add_argument("-w", "--workers", action='store', dest='gun_workers', help="Number of gunicorn workers for REST API"), required=False)
    return parser

def parse_args():
    if not args.kafka and not args.nats and not args.restapi:
        print("No run method option specified. Please choose either (-k)Kafka, (-n)Nats or (-r)REST")
        sys.exit(1)
    else:
        if args.kafka:
            if args.target_server and args.sub_topic and args.pub_topic:
                print("Sweet! Kafka mode initialized")
            else:
                print("No target, sub topic or pub topic")
                sys.exit(1)
        elif args.nats:
            if args.target_server and args.sub_topic and args.pub_topic:
                print("Sweet! NATS mode initialized")
                sys.exit(1)
        elif args.restapi:
            

app = falcon.API()
classification = Classify()
app.add_route('/api/classify', classification)