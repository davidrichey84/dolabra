import time,sys
from kafka import KafkaConsumer
from kafka import KafkaProducer

class KafkaNER(object):
    def __init__(self, params):
        params = params
        kafka_consumer = self._kafka_consumer_init(params)
        kafka_producer = self._kafka_producer_init(params)
        ner_model = self._load_ner_model(params)

    def _kafka_consumer_init(self, params):
        kafka_brokers = params['target']
        kafka_input_topic = params['sub_topic']
        groupid = params.get('groupid', 'dolabra')
        offset = params.get('offset', 'earliest')
        autocommit = params.get('autocommit', True)
        sasl_plain_username = params.get('sasl_plain_username', '')
        sasl_plain_password = params.get('sasl_plain_password', '')

        try:
            consumer = KafkaConsumer(kafka_input_topic,
                                    group_id = groupid,
                                    bootstrap_servers = kafka_brokers,
                                    auto_offset_reset = offset,
                                    enable_auto_commit = autocommit,
                                    security_protocol = 'SASL_PLAINTEXT',
                                    sasl_mechanism = 'PLAIN',
                                    sasl_plain_username = sasl_plain_username,
                                    sasl_plain_password = sasl_plain_password)
            return consumer
        except Exception as e:
            print("Failed to initialize the consumer: {}".format(str(e)))
            sys.exit(1)
        
    def _kafka_producer_init(self, params):
        kafka_brokers = params['target']
        kafka_output_topic = params['pub_topic']
        groupid = params.get('groupid', 'dolabra')
        offset = params.get('offset', 'earliest')
        autocommit = params.get('autocommit', True)
        sasl_plain_username = params.get('sasl_plain_username', '')
        sasl_plain_password = params.get('sasl_plain_password', '')

        try:
            producer = KafkaProducer(bootstrap_servers = kafka_brokers,
                                    acks = 0,
                                    batch_size = 655360,
                                    linger_ms = 100,
                                    security_protocol = 'SASL_PLAINTEXT',
                                    sasl_mechanism = 'PLAIN',
                                    sasl_plain_username = sasl_plain_username,
                                    sasl_plain_password = sasl_plain_password)
            return producer
        except Exception as e:
            print("Failed to initialize the producer: {}".format(str(e)))
            sys.exit(1)
        
    def _kafka_publish(self, message):
        msg_as_bytes = str.encode(message)
        try:
            self.kafka_producer.send(self.topic, msg_as_bytes)
        except Exception as e:
            # really need to get some logging here!
            print("Could not publish message {}: {}".format(message, str(e)))

    def message_loop(self):
        for message in self.kafka_consumer:
            classifed_message = _classify_message(message)
            self._kafka_publish(classified_message)
        
    def _classify_message(self, message):
        classify_log = self.ner_model(message)
        if classify_log and len(classify_log) >1:
            payload = {'results': []}
            for item in classify_log.ents:
                payload['results'].append({item.label_: item.text})
        return payload

        