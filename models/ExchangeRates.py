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
    
    def get_all(self):
        conn = Db().connect_to_db()
        cur = conn.cursor()
        get_all_pairs_query = '''
            SELECT er.id,
                c1.id as base_currency_id,
                c1.code AS base_currency_code, 
                c1.full_name AS base_currency_full_name, 
                c1.sign AS base_currency_sign, 
                c2.id as target_currency_id,
                c2.code AS target_currency_code, 
                c2.full_name AS target_currency_full_name, 
                c2.sign AS target_currency_sign, 
                er.rate
            FROM exchange_rates er
            JOIN currencies c1 ON er.base_currency_id = c1.id
            JOIN currencies c2 ON er.target_currency_id = c2.id;
        '''

        cur.execute(get_all_pairs_query)
        pairs = cur.fetchall()
        conn.commit()

        cur.close()
        conn.close()
        return pairs
