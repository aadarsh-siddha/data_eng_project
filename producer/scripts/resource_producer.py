import os
import csv
import sys
import argparse
import importlib
from time import sleep
from typing import Dict
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField

def parse_args():
    parser = argparse.ArgumentParser(description="Upload data to schema registry.")
    parser.add_argument("--csv", required=True, help="Directory containing CSV files")
    parser.add_argument("--schema", required=True, help="Directory containing Avro schema files")
    parser.add_argument("--class_path", required=True, help="Python file or module for the record object class")
    parser.add_argument("--config", required=True, help="Path to Confluent Cloud client config")
    parser.add_argument("--registry", required=True, help="Path to schema registry config")
    parser.add_argument("--resource", required=True, help="Resource name (e.g., patient, abc)")

    return parser.parse_args()


def read_config(file_path):
  # reads the client configuration from client.properties
  # and returns it as a key-value map
  config = {}
  with open(file_path) as fh:
    for line in fh:
      line = line.strip()
      if len(line) != 0 and line[0] != "#":
        parameter, value = line.strip().split('=', 1)
        config[parameter] = value.strip()
  return config

def read_schema_registry_config(file_path):
    config = {}
    with open(file_path) as fh:
        key = None
        for line in fh:
            line = line.strip()
            if not line or line.startswith("="):
                continue
            if line.endswith(":"):
                key = line[:-1].strip()
            elif key:
                config[key] = line
                key = None
    new_dict = {}
    new_dict['url'] = config['Endpoint']
    new_dict['basic.auth.user.info'] = config['API key'] + ':' + config['API secret']
    return new_dict

def get_record_module(resource: str):
    module_name = f"{resource}_record"
    if resource.endswith('s') and resource not in ['allergies','supplies','imaging_studies']:
        resource = resource[:-1]
    class_name = f"{resource.capitalize()}Record"
    func_name = f"{resource}_record_to_dict"

    try:
        module = importlib.import_module(module_name)
        RecordClass = getattr(module, class_name)
        to_dict_func = getattr(module, func_name)
        return RecordClass, to_dict_func
    except (ModuleNotFoundError, AttributeError) as e:
        raise ImportError(f"Could not load resource module for '{resource}': {e}")


class PatientProducer():
    def __init__(self, kafka_config: Dict,schema_registry_config: Dict, extra_config: Dict):
        value_schema_str = self.load_schema(extra_config['RESOURCE_VALUE_SCHEMA'])
        schema_registry_client = SchemaRegistryClient(schema_registry_config)
        self.key_serializer = StringSerializer('utf_8')
        self.value_serializer = AvroSerializer(schema_registry_client, value_schema_str, extra_config['resource_to_dict_func'])

        self.producer = Producer(kafka_config)


    @staticmethod
    def load_schema(schema_path: str):
        with open(f"{schema_path}") as f:
            schema_str = f.read()
        return schema_str

    @staticmethod
    def read_records(resource_path: str, RecordClass):
        records= []
        with open(resource_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)  # skip the header
            for row in reader:
                records.append(RecordClass(row))
        return records

    @staticmethod
    def delivery_report(err, msg):
        if err is not None:
            print("Delivery failed for record {}: {}".format(msg.key(), err))
            return
        print('Record {} successfully produced to {} [{}] at offset {}'.format(
            msg.key(), msg.topic(), msg.partition(), msg.offset()))

    def publish(self, topic: str, records: []):
        for value in records:
            try:
                self.producer.produce(topic=topic,
                                      key=self.key_serializer(topic, SerializationContext(topic=topic,
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
    args = parse_args()
    
    csv_file_dir = args.csv
    schema_file_dir = args.schema
    object_class_dir = args.class_path
    config_file_path = args.config
    schema_registry_file_path = args.registry
    resource_name = args.resource


    RESOURCE_FILE = csv_file_dir+'/'+resource_name+'.csv'
    RESOURCE_VALUE_SCHEMA = schema_file_dir+'/'+resource_name+'.avsc'
    kafka_config = read_config(config_file_path)
    schema_registry_config = read_schema_registry_config(schema_registry_file_path)
    
    RecordClass, to_dict_func = get_record_module(resource_name)
    extra_config = {'RESOURCE_VALUE_SCHEMA': RESOURCE_VALUE_SCHEMA, 'resource_to_dict_func': to_dict_func}


    producer = PatientProducer(kafka_config,schema_registry_config, extra_config)
    resource_records = producer.read_records(RESOURCE_FILE, RecordClass)
    producer.publish(topic=resource_name, records=resource_records)