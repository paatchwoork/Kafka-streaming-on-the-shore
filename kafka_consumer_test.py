from confluent_kafka import Consumer, KafkaError

# Kafka consumer configuration
conf = {
    'bootstrap.servers':'localhost:9092',  # Kafka broker address (where is kafka running?)
    'group.id': 'my_consumer_group',        # Set a consumer group ID
    'auto.offset.reset': 'earliest'         # Start consuming from the earliest available offset
}

# Create Kafka consumer instance
consumer = Consumer(conf)

# Subscribe to Kafka topic
consumer.subscribe(['delhaize_shop'])

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
                print(msg.error())
                break

        # Print message value
        print(msg.value().decode('utf-8'))  # Assuming messages are UTF-8 encoded

finally:
    # Close Kafka consumer
    consumer.close()