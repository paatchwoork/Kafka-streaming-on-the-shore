import psycopg2

ENDPOINT = "database-2.chwckuee0smq.eu-central-1.rds.amazonaws.com"
PORT = "5432"
USER = "postgres"
DBNAME = "postgres"
SSL_CERTIFICATE = "./eu-central-1-bundle.pem"

try:
    conn = psycopg2.connect(
        host=ENDPOINT,
        port=PORT,
        database=DBNAME,
        user=USER,
        password="postgres",
        sslrootcert=SSL_CERTIFICATE
    )
    cur = conn.cursor()

    with open("./create_tables.sql", "r") as sql_file:
        sql_script = sql_file.read()

    # Execute the SQL script
    cur.execute(sql_script)

    # Commit the transaction
    conn.commit()
    print("Tables created successfully")

except Exception as e:
    print("Failed to create tables:", e)

finally:
    # Close cursor and connection
    if cur:
        cur.close()
    if conn:
        conn.close()
