import os
import psycopg2 as psycopg2

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get DB URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Expose a connection for use in other files
def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def get_db_status():
  connection = get_db_connection()
  cursor = connection.cursor()

  cursor.execute("SELECT NOW();")
  now = cursor.fetchone()
  cursor.close()

  return {"status":"connected", "now":now}

def initialize_table():
  connection = get_db_connection()
  cursor = connection.cursor()
  cursor.execute('''
      CREATE TABLE IF NOT EXISTS Concall_links (
          ID SERIAL PRIMARY KEY,
          TickerName VARCHAR(100),
          Links JSONB
      );
  ''')
  connection.commit()
  cursor.close()
  print("Table ready")
