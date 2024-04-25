from Db import Db


class ExchangeRatesModule:

    def create(self, base_currency_id, target_currency_id, rate):
        conn = Db().connect_to_db()
        cur = conn.cursor()

        create_currency_query = '''
            INSERT INTO exchange_rates (base_currency_id, target_currency_id, rate) 
            VALUES (%s, %s, %s)
            RETURNING id;
        '''

        cur.execute(create_currency_query, (base_currency_id, target_currency_id, rate))
        created_pair_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return created_pair_id
