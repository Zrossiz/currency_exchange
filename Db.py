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
                id SERIAL PRIMARY KEY,
                base_currency_id INTEGER REFERENCES currencies (id),
                target_currency_id INTEGER REFERENCES currencies (id),
                rate DECIMAL(10, 6)
            );
        '''

        cur.execute(create_table_query)
        conn.commit()
        cur.close()
        conn.close()

#Db().create_tables(Db().connect_to_db())