from confluent_kafka import Consumer, KafkaError
import json
import psycopg2

# Kafka consumer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker(s) address
    'group.id': 'my_consumer_group',        # Consumer group ID
    'auto.offset.reset': 'earliest'         # Start consuming from the earliest available offset
}

# Create Kafka consumer
consumer = Consumer(conf)

# Subscribe to Kafka topic
consumer.subscribe(['delhaize_shop'])

# Database connection parameters
db_params = {
    'host': 'database-2.chwckuee0smq.eu-central-1.rds.amazonaws.com',
    'port': '5432',
    'database': 'database-2',
    'user': 'postgres',
    'password': 'postgres'
}
# Connect to PostgreSQL database
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

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

        # Process message
        try:
            # Parse message value (assuming it's JSON)
            data = json.loads(msg.value())

            # Insert data into PostgreSQL database
            cur.execute("""
                INSERT INTO your_table (column1, column2, ...)
                VALUES (%s, %s, ...)
            """, (data['column1'], data['column2'], ...))

            # Commit transaction
            conn.commit()
        except Exception as e:
            # Handle error
            print(f"Error processing message: {str(e)}")
            conn.rollback()

finally:
    # Close Kafka consumer and database connection
    consumer.close()
    cur.close()
    conn.close()
