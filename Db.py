import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


class Db:
    def connect_to_db(self):
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('USER')
        db_password = os.getenv('PASSWORD')
        db_host = os.getenv('HOST')
        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
        return conn

    def create_tables(self, conn):
        cur = conn.cursor()

        create_table_query = '''
        CREATE TABLE currencies (
            id SERIAL PRIMARY KEY,
            code VARCHAR,
            full_name VARCHAR,
            sign VARCHAR
        );
        
        CREATE TABLE exchange_rates (
            id INTEGER PRIMARY KEY,
            base_currency_id INTEGER REFERENCES currencies (id),
            target_currency_id INTEGER REFERENCES currencies (id),
            Rate DECIMAL(6)
        );
        '''

        cur.execute(create_table_query)
        conn.commit()
        cur.close()
        conn.close()

    def create_currency(self, code, full_name, sign):
        conn = self.connect_to_db()
        cur = conn.cursor()

        create_currency_query = f'''
            INSERT INTO currencies (code, full_name, sign)
            VALUES (%s, %s, %s)
        '''

        cur.execute(create_currency_query, (code, full_name, sign))
        conn.commit()
        cur.close()
        conn.close()

