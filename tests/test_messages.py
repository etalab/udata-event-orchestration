import json
from datetime import date
from dateutil.parser import parse as parse_dt
import time

from kafka import TopicPartition
import pytest


PREFIX_TOPIC = 'udata'

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

    # consumer.subscribe([f'{PREFIX_TOPIC}.resource.analysed', f'{PREFIX_TOPIC}.resource.stored', f'{PREFIX_TOPIC}.resource.stored'])
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

    # TODO: Slightly more than SLEEP_BETWEEN_BATCHES set in udata-hydra
    SLEEP_BETWEEN_BATCHES = 10
    time.sleep(SLEEP_BETWEEN_BATCHES + 1)

    consumed = consumer.poll(1000 * (SLEEP_BETWEEN_BATCHES + 1))
    
    assert len(consumed[tp_analysed]) == 2
    assert len(consumed[tp_stored]) == 1
    assert len(consumed[tp_checked]) == 1

    analysed_hydra = json.loads(consumed[tp_analysed][0].value)
    assert analysed_hydra['service'] == 'udata-hydra'
    assert analysed_hydra == get_message(messages, 'resource.analysed', resource_type, 'udata-hydra')['message']

    analysed_detective = json.loads(consumed[tp_analysed][1].value)
    assert analysed_detective['service'] == 'csvdetective'
    assert analysed_detective == get_message(messages, 'resource.analysed', resource_type, 'csvdetective')['message']

    stored = json.loads(consumed[tp_stored][0].value)
    assert stored == get_message(messages, 'resource.stored', resource_type)['message']

    checked = json.loads(consumed[tp_checked][0].value)
    assert parse_dt(checked['value'].pop('check_date')).date() == date.today()
    checked['value'].pop('headers')
    checked['value'].pop('response_time')
    checked_expect = get_message(messages, 'resource.checked', resource_type)['message']
    checked_expect['value'].pop('check_date')
    checked_expect['value'].pop('headers')
    checked_expect['value'].pop('response_time')
    assert checked == checked_expect
