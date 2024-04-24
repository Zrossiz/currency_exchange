from Db import Db


class CurrencyModel:

    def create_currency(self, code, full_name, sign):
        conn = Db().connect_to_db()
        cur = conn.cursor()

        print('Code: ', code)
        print('Full name: ', full_name)
        print('Sign: ', sign)

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
