import sys
from argparse import ArgumentParser
import logging
#from lib import kafka_ner
from lib import rest_ner


def setup_logging(level='DEBUG'):
    global LOG
    LOG = logging.getLogger("dolabra")
    LOG.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(formatter)
    LOG.addHandler(ch)

def setup_arg_parser():
    parser = ArgumentParser()
    parser.add_argument("-k", "--kafka", action='store_true', help="Kafka message queue mode", required=False)
    parser.add_argument("-n", "--nats", action='store_true', help="Nats message queue mode", required=False)
    parser.add_argument("-t", "--target", action='store', dest='target_server', help="Target kafka/NATS server:port", required=False)
    parser.add_argument("-st", "--subtopic", action='store', dest='sub_topic', help="Subscription topic you would like to subscribe to", required=False)
    parser.add_argument("-pt", "--pubtopic", action='store', dest='pub_topic', help="Publish topic you would like to publish results to", required=False)
    parser.add_argument("-r", "--restapi", action='store_true', help="REST API mode", required=False)
    parser.add_argument("-b", "--bind", action='store', dest='bind', help="Interface and port to bind REST API. ex: 0.0.0.0:5000", required=False)
    parser.add_argument("-w", "--workers", action='store', dest='gun_workers', help="Number of gunicorn workers for REST API", required=False)
    return parser

def parse_args():
    if not args.kafka and not args.nats and not args.restapi:
        print("No run method option specified. Please choose either (-k)Kafka, (-n)Nats or (-r)REST")
        sys.exit(1)
    else:
        if args.kafka:
            if args.target_server and args.sub_topic and args.pub_topic:
                print("Sweet! Kafka mode initialized")
                kafka_ner.KafkaNER(args)
            else:
                print("No target, sub topic or pub topic")
                sys.exit(1)
        elif args.nats:
            if args.target_server and args.sub_topic and args.pub_topic:
                print("Not implemented yet")
                sys.exit(1)
        elif args.restapi:
            rest_ner.REST(args)
if __name__ == '__main__':
    parser = setup_arg_parser()
    args = parser.parse_args()
    parse_args()