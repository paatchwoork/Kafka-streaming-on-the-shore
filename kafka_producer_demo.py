from confluent_kafka import Producer

# Kafka producer configuration
conf = {'bootstrap.servers': 'localhost:9092'}  # Change to your Kafka broker address

# Create Kafka producer
producer = Producer(conf)

# Produce messages to Kafka topic
for i in range(10):
    producer.produce('delhaize_shop', key=str(i), value=f'Message {i}')

# Flush producer queue to ensure all messages are sent
producer.flush()
