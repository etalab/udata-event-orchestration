import json
from datetime import date
from dateutil.parser import parse as parse_dt
import os
import time

from kafka import TopicPartition
import pytest


PREFIX_TOPIC = 'udata'

# Override this value with an env variable if you have a different value in udata-hydra crawler
SLEEP_BETWEEN_BATCHES = int(os.environ.get("SLEEP_BETWEEN_BATCHES", 60))


def get_message(messages, topic, resource_type, service=None):
    '''
    Return first message matching topic and resource_type
    '''
    messages = [m for m in messages if m['topic'] == topic and m['type'] == resource_type]
    if not service:
        return messages[0]
    return [m for m in messages if m['message']['service'] == service][0]


def test_send_available_resource_created(producer, consumer, messages):

    resource_type = 'available-csv'
    sending_message = get_message(messages, 'resource.created', resource_type)
    dataset_id = sending_message['message']['meta']['dataset_id']
    resource_id = sending_message['key']
    resource_url = sending_message['message']['value']['url']

    # Prepare consumer
    tp_analysed = TopicPartition(f'{PREFIX_TOPIC}.resource.analysed', 0)
    tp_stored = TopicPartition(f'{PREFIX_TOPIC}.resource.stored', 0)
    tp_checked = TopicPartition(f'{PREFIX_TOPIC}.resource.checked', 0)
    consumer.assign([tp_analysed, tp_stored, tp_checked])
    consumer.seek_to_end()
    consumer.poll()

    sent = producer.send(f'{PREFIX_TOPIC}.{sending_message["topic"]}',
                   value=sending_message['message'],
                   key=bytes(sending_message['key'],encoding='utf8')
    )

    # Make sure that udata-hydra crawler has time to crawl the url
    time.sleep(SLEEP_BETWEEN_BATCHES + 1)

    # Poll messages
    consumed = consumer.poll(1000 * (SLEEP_BETWEEN_BATCHES + 1))
    
    # Assert expected number of messages have been consumed
    assert len(consumed[tp_analysed]) == 2
    assert len(consumed[tp_stored]) == 1
    assert len(consumed[tp_checked]) == 1

    # Assert analysed message sent by hydra service
    analysed_hydra = json.loads(consumed[tp_analysed][0].value)
    assert analysed_hydra['service'] == 'udata-hydra'
    assert analysed_hydra == get_message(messages, 'resource.analysed', resource_type, 'udata-hydra')['message']

    # Assert analysed message sent by csv detective
    analysed_detective = json.loads(consumed[tp_analysed][1].value)
    assert analysed_detective['service'] == 'csvdetective'
    assert analysed_detective == get_message(messages, 'resource.analysed', resource_type, 'csvdetective')['message']

    # Assert stored message
    stored = json.loads(consumed[tp_stored][0].value)
    assert stored == get_message(messages, 'resource.stored', resource_type)['message']

    # Assert checked message, ignoring date-dependent values
    checked = json.loads(consumed[tp_checked][0].value)
    assert parse_dt(checked['value'].pop('check_date')).date() == date.today()
    checked['value'].pop('headers')
    checked['value'].pop('response_time')
    checked_expect = get_message(messages, 'resource.checked', resource_type)['message']
    checked_expect['value'].pop('check_date')
    checked_expect['value'].pop('headers')
    checked_expect['value'].pop('response_time')
    assert checked == checked_expect
