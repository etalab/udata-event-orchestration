from email.policy import default
import logging
import click
import os
from kafka import KafkaConsumer, KafkaProducer
import json

with open('messages.json') as fp:
    messages = json.load(fp)

KAFKA_HOST = os.environ.get("KAFKA_HOST", "localhost")
KAFKA_PORT = os.environ.get("KAFKA_PORT", "9092")

PREFIX_TOPIC = os.environ.get("UDATA_INSTANCE_NAME", "udata")

@click.group()
@click.version_option()
def cli():
    """
    udata-kafka-event-testing
    """

@cli.command()
def consume():
    logging.basicConfig(level=logging.INFO)
    print('coucou')
    consumer = KafkaConsumer(bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}", group_id='toto')
    consumer.subscribe([PREFIX_TOPIC+'.'+x['topic'] for x in messages])
    for message in consumer:
        try:
            val  = message.value
            val_utf8 = val.decode("utf-8").replace("NaN","null")
            data = json.loads(val_utf8)
            logging.info('Topic : ' + message.topic)
            logging.info('Message key : ' + message.key.decode('utf-8'))
            logging.info(json.dumps(data, indent=4))
            logging.info(' ----------- ')
        except:
            pass



@click.option('-t', '--topic', default='resource.created',
              help='Topic on which send message')
@click.option('-s', '--service', default=None,
              help='Service which send the message')
@click.option('-mt', '--message_type', default=None,
              help='Message type')
@cli.command()
def produce(topic, service, message_type):
    selection = []
    list_services = []
    list_message_types = []

    selection = [s for s in messages if s['topic'] == topic]

    if service:
        selection = [s for s in selection if s['message']['service'] == service]
    else:
        list_services = list(dict.fromkeys([s['message']['service'] for s in selection]))
        if len(list_services) > 1:
            value = click.prompt('Which service ?\n{}\nChose '.format('\n'.join(list_services), type=str))
            if value in list_services:
                selection = [s for s in selection if s['message']['service'] == value]
            else:
                print('not in list - abort')


    if message_type:
        selection = [s for s in selection if s['type'] == message_type]
    else:
        list_message_types = list(dict.fromkeys([s['type'] for s in selection]))
        if len(list_message_types) > 1:
            value = click.prompt('Which message type ?\n{}\nChose '.format('\n'.join(list_message_types), type=str))
            if value in list_message_types:
                selection = [s for s in selection if s['type'] == value]
            else:
                print('not in list - abort')
    

    for message in selection:
        #logging.basicConfig(level=logging.INFO)
        producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        topic = topic
        producer.send(PREFIX_TOPIC+'.'+topic, value=message['message'], key=bytes(message['key'],encoding='utf8'))
