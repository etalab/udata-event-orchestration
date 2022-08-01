from kafka import KafkaProducer, KafkaConsumer
import json
import os

import pytest


KAFKA_HOST = os.environ.get("KAFKA_HOST", "localhost")
KAFKA_PORT = os.environ.get("KAFKA_PORT", "9092")

@pytest.fixture
def messages():
    with open("udata_event_orchestration/messages.json", "r") as f:
        return json.load(f)

@pytest.fixture
def producer():
    producer = KafkaProducer(bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}", value_serializer=lambda v: json.dumps(v).encode("utf-8"))
    return producer

@pytest.fixture
def consumer():
    consumer = KafkaConsumer(bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}", group_id="test", enable_auto_commit=True)
    return consumer
