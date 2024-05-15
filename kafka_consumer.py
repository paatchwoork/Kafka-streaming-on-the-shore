import logging
from confluent_kafka import Consumer, KafkaError
import json
from kafka_on_the_cloud import CloudManager
from worker import worker

# Configuring the logger

logging.basicConfig(
    format="%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d :: %(message)s",
    level=logging.INFO,
    filename="consumer.log",
)

conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "my_consumer_group",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(conf)

consumer.subscribe(["delhaize_shop"])

cloud_manager = CloudManager(
    endpoint="database-2.chwckuee0smq.eu-central-1.rds.amazonaws.com",
    port="5432",
    user="postgres",
    password="postgres",
    dbname="postgres",
    ssl_certificate="./eu-central-1-bundle.pem",
)

# Consume messages from Kafka topic
try:
    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition
                continue
            else:
                logging.error(f"Kafka error: {msg.error()}")
                break

        # Process message
        try:
            data = json.loads(msg.value())

            processed_data = worker(data)

            # Insert data into the database
            success = cloud_manager.insert_data(processed_data)
            if success:
                logging.info("Data inserted successfully")
            else:
                logging.error("Failed to insert data")

        except Exception as e:
            logging.error(f"Error processing message: {str(e)}")

finally:
    consumer.close()
  