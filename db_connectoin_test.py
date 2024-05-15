import psycopg2

ENDPOINT = "database-2.chwckuee0smq.eu-central-1.rds.amazonaws.com"
PORT = "5432"
USER = "postgres"
REGION = "eu-central-1b"
DBNAME = "postgres"
SSL_CERTIFICATE = "./eu-central-1-bundle.pem"

try:
    conn = psycopg2.connect(
        host=ENDPOINT,
        port=PORT,
        database=DBNAME,
        user=USER,
        password="postgres",
        sslrootcert=SSL_CERTIFICATE,
    )
    cur = conn.cursor()
    cur.execute("""SELECT now()""")
    query_results = cur.fetchall()
    print(query_results)
except Exception as e:
    print("Database connection failed due to {}".format(e))
