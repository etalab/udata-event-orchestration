import pandas as pd
import random
from kafka import KafkaProducer
import json
import sys

producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
df = pd.read_csv('export-resource.csv', sep=";")

df = df[df['format'] == 'csv']

for index, row in df.sample(frac=1)[:int(sys.argv[1])].iterrows():
    message = {}
    message['key'] = row['id']
    message['type'] = row['format']
    message['topic'] = "resource.created"
    message['message'] = {}
    message['message']['service'] = 'udata'
    message['message']['value'] = {}
    message['message']['value']['resource'] = row.to_dict()
    message['message']['meta'] = {}
    message['message']['meta']['dataset_id'] = row['dataset.id']
    producer.send("resource.created", value=message['message'], key=bytes(message['key'],encoding='utf8'))
    print(message['message'])
print('all done')