from Db import Db


class CurrencyModel:

    def get_all(self):
        conn = Db().connect_to_db()
        cur = conn.cursor()

        get_all_currencies = '''
            SELECT id, full_name, code, sign FROM currencies
        '''

        cur.execute(get_all_currencies)
        currencies = cur.fetchall()

        cur.close()
        conn.close()

        return currencies

    def get_by_slug(self, slug):
        conn = Db().connect_to_db()
        cur = conn.cursor()
        get_currency_query = f'''
            SELECT id, full_name, code, sign FROM currencies WHERE code = %s
        '''

        cur.execute(get_currency_query, (slug,))
        currency = cur.fetchone()
        cur.close()
        conn.close()

        return currency

    def create_currency(self, code, full_name, sign):
        conn = Db().connect_to_db()
        cur = conn.cursor()

        create_currency_query = f'''
            INSERT INTO currencies (code, full_name, sign)
            VALUES (%s, %s, %s)
        '''

        cur.execute(create_currency_query, (code, full_name, sign))
        conn.commit()
        cur.close()
        conn.close()

        response_data = {
            "success": "true",
            "data": {
                "code": code,
                "name": full_name,
                "sign": sign
            }
        }

        return response_data
