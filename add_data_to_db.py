import logging
import psycopg2
from datetime import date

#logging library is for the sake of testing

logging.basicConfig(format='%(name)s:[%(levelname)s] %(message)s',  level=logging.DEBUG)
log = logging.getLogger(__name__)

conn = psycopg2.connect(
    host="0.0.0.0",
    database="deltatask3",
    user="postgres",
    password="postgres",
    port=5432
)

cursor = conn.cursor()
log.info(f"Connected to database: {cursor}")

def initialize_tables():
    """
    Creates tables if they do not exist.
    Returns true if the tables were create from this call, 
    and false if they alreadt existed.
    """
    query = """
    CREATE TABLE IF NOT EXISTS studentdetails (
            name VARCHAR(50) PRIMARY KEY,
            password VARCHAR(50)
    );
    """
    cursor.execute(query)
    conn.commit()
    log.info("Created table userDatabase.")

def add_users():
    cursor.execute(
                "INSERT INTO studentdetails VALUES (thomas,password) ON CONFLICT DO NOTHING",
            )
    cursor.execute(
                    "INSERT INTO studentdetails VALUES (avishek,password) ON CONFLICT DO NOTHING",
                )
    conn.commit()
            
    log.info("Inserted data into table userDatabase.")


initialize_tables()
add_users()