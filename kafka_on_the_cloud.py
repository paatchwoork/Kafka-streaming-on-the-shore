import psycopg2
import logging

logging.basicConfig(
    format="%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d :: %(message)s",
    level=logging.INFO,
    filename="consumer.log",
)


class CloudManager:
    def __init__(self, endpoint, port, user, password, dbname, ssl_certificate):
        self.endpoint = endpoint
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.ssl_certificate = ssl_certificate

    def connect_to_db(self):
        try:
            conn = psycopg2.connect(
                host=self.endpoint,
                port=self.port,
                database=self.dbname,
                user=self.user,
                password=self.password,
                sslrootcert=self.ssl_certificate,
            )
            logging.info("Connected to the database successfully")
            return conn
        except Exception as e:
            logging.error("Failed to connect to the database: %s", e)
            return None

    def create_tables(self):
        conn = self.connect_to_db()
        if conn:
            try:            
                cur = conn.cursor()

                with open("./create_tables.sql", "r") as sql_file:
                    schema= sql_file.read()

                # Execute the SQL script
                cur.execute(schema)

                # Commit the transaction
                conn.commit()
                logging.info("Tables created successfully")

            except Exception as e:
                logging.error("Failed to create tables: %s", e)

            finally:
                # Close cursor and connection
                if cur:
                    cur.close()
                self.close_connection(conn)
        else:
            logging.error("Failed to connect to the database")

    def insert_data(self, data):
        conn = self.connect_to_db()
        if conn:
            try:
                # Insert purchase data into the purchases table
                purchase_query = "INSERT INTO purchases (store, date, total_price) VALUES (%s, %s, %s) RETURNING id"
                purchase_params = (
                    data["store"],
                    data["date"],
                    data["total_price"],
                )

                cur = conn.cursor()
                cur.execute(purchase_query, purchase_params)
                purchase_id = cur.fetchone()[0]

                # Insert products data into the products table
                products = data["products"]
                for product in products:
                    product_query = "INSERT INTO products (purchase_id, name, category, price) VALUES (%s, %s, %s, %s)"
                    product_params = (
                        purchase_id,
                        product["name"],
                        product["category"],
                        product["price"],
                    )
                    cur.execute(product_query, product_params)

                conn.commit()
                cur.close()
                self.close_connection(conn)
                return True

            except Exception as e:
                logging.error("Failed to insert data: %s", e)
                return False

        else:
            logging.error("Failed to connect to the database")
            return False

    def execute_query(self, query):
        conn = self.connect_to_db()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(query)
                conn.commit()
                cur.close()
                logging.info("Query executed successfully")
                self.close_connection(conn)
                return True

            except Exception as e:
                logging.error("Failed to execute query: %s", e)
                return False
        else:
            logging.error("Failed to connect to the database")
            return False

    def close_connection(self, conn):
        try:
            if conn:
                conn.close()
                logging.info("Database connection closed successfully")

        except Exception as e:
            logging.error("Failed to close database connection:%s", e)
