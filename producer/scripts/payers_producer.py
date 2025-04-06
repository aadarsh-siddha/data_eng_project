import os
import csv
from time import sleep
from typing import Dict
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from payers_record import PayerRecord, payer_record_to_dict
from settings import SCHEMA_REGISTRY_URL, BOOTSTRAP_SERVERS

PAYERS_FILE = "../synthea/output/csv/payers.csv"
PAYERS_VALUE_SCHEMA = "../resources/schemas/payers.avsc"
TOPIC = "payer"

class PayerProducer():
    def __init__(self, props: Dict):
        value_schema_str = self.load_schema(props['schema.value'])
        schema_registry_props = {'url': props['schema_registry.url']}
        schema_registry_client = SchemaRegistryClient(schema_registry_props)
        self.key_serializer = StringSerializer('utf_8')
        self.value_serializer = AvroSerializer(schema_registry_client, value_schema_str, payer_record_to_dict)

        # Producer Configuration
        producer_props = {'bootstrap.servers': props['bootstrap.servers']}
        self.producer = Producer(producer_props)


    @staticmethod
    def load_schema(schema_path: str):
        with open(f"{schema_path}") as f:
            schema_str = f.read()
        return schema_str

    @staticmethod
    def read_records(resource_path: str):
        records= []
        with open(resource_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)  # skip the header
            for row in reader:
                records.append(PayerRecord(row))
        return records

    @staticmethod
    def delivery_report(err, msg):
        if err is not None:
            print("Delivery failed for record {}: {}".format(msg.key(), err))
            return
        print('Record {} successfully produced to {} [{}] at offset {}'.format(
            msg.key(), msg.topic(), msg.partition(), msg.offset()))

    def publish(self, topic: str, records: [PayerRecord]):
        for value in records:
            try:
                self.producer.produce(topic=topic,
                                      key=self.key_serializer("payer", SerializationContext(topic=topic,
                                                                                        field=MessageField.KEY)),
                                      value=self.value_serializer(value, SerializationContext(topic=topic,
                                                                                              field=MessageField.VALUE)),
                                      on_delivery=self.delivery_report)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Exception while producing record - {value}: {e}")

        self.producer.flush()
        sleep(1)

if __name__ == "__main__":
    config = {
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'schema_registry.url': SCHEMA_REGISTRY_URL,
        'schema.value': PAYERS_VALUE_SCHEMA
    }
    producer = PayerProducer(props=config)
    records = producer.read_records(resource_path=PAYERS_FILE)
    producer.publish(topic=TOPIC, records=records)