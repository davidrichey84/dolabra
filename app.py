import sys
from argparse import ArgumentParser
import logging
from lib import kafka_ner
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
    subparsers = parser.add_subparsers()
    return parser, subparsers

def setup_kafka_subparser(subparsers):
    parser_kafka = subparsers.add_parser('kafka')
    parser_kafka.add_argument('-t', '--target', action='store', dest='target', help='target:port', required=True)
    parser_kafka.add_argument('-st', '--subtopic', action='store', dest='sub_topic', help='Subscription topic', required=True)
    parser_kafka.add_argument('-pt', '--pubtopic', action='store', dest='pub_topic', help='Publish topic', required=True)
    return subparsers, parser_kafka

def setup_nats_subparser(subparsers):
    parser_nats = subparsers.add_parser('nats')
    parser_nats.add_argument('-t', '--target', action='store', dest='target', help='target:port', required=True)
    parser_nats.add_argument('-st', '--subtopic', action='store', dest='sub_topic', help='subscription topic', required=True)
    parser_nats.add_argument('-pt', '--pubtopic', action='store', dest='pub_topic', help='publish topic', required=True)
    return subparsers, parser_nats

def setup_rest_subparser(subparsers):
    parser_rest = subparsers.add_parser('rest')
    parser_rest.add_argument('-b', '--bind', action='store', dest='bind', help='Interface and port to bind REST API. ex: 0.0.0.0:5000', required=True)
    parser_rest.add_argument('-w', '--workers', action='store', dest='gun_workers', help='Number of gunicorn workers for REST API', required=True)
    return subparsers, parser_rest

def kafka(args):
    kafka_ner.KafkaNER(args)

def nats(args):
    print("This feature has not yet been implemented...")
    sys.exit(1)

def rest(args):
    rest_ner.REST(args)


if __name__ == '__main__':
    parser, subparsers = setup_arg_parser()
    subparsers, parser_kafka = setup_kafka_subparser(subparsers)
    # Not yet implemented
    #subparsers, parser_nats = setup_nats_subparser(subparsers)
    subparsers, parser_rest = setup_rest_subparser(subparsers)
    parser.parse_args()