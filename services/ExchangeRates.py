from models.ExchangeRates import ExchangeRatesModel
from Db import Db


class ExchangeRatesService:

    def create(self, base_currency_code, target_currency_code, rate):
        base_currency = self._find_currencies_by_code(base_currency_code)[0]
        target_currency = self._find_currencies_by_code(target_currency_code)[0]

        new_currency_pair_id = ExchangeRatesModel().create(
            base_currency[0], target_currency[0], rate)

        response_data = {
            "id": new_currency_pair_id,
            "baseCurrency": {
                "id": base_currency[0],
                "name": base_currency[2],
                "code": base_currency[1],
                "sign": base_currency[3],
            },
            "targetCurrency": {
                "id": target_currency[0],
                "name": target_currency[2],
                "code": target_currency[1],
                "sign": target_currency[3],
            },
            "rate": rate
        }

        return response_data
    
    def get_all(self):
        currencies = ExchangeRatesModel().get_all()
        response_data = []
        for pair in currencies:
            formatted_pair = {
                "id": pair[0],
                "baseCurrency": {
                    "id": pair[1],
                    "name": pair[3],
                    "code": pair[2],
                    "sign": pair[4],
                },
                "targetCurrency": {
                    "id": pair[5],
                    "name": pair[7],
                    "code": pair[6],
                    "sign": pair[8],
                },
                "rate": float(pair[9]),
            }
            response_data.append(formatted_pair)
        return response_data

    def _find_currencies_by_code(self, code):
        conn = Db().connect_to_db()
        cur = conn.cursor()

        find_currencies_query = '''
            select * from currencies where code = %s;
        '''

        cur.execute(find_currencies_query, (code,))
        currency_sql = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()

        return currency_sql
    
    def get_by_slug(self, base, target):
        pair = ExchangeRatesModel().get_by_slug(base, target)[0]
        formatted_pair = {
            "id": pair[0],
            "baseCurrency": {
                "id": pair[1],
                "name": pair[3],
                "code": pair[2],
                "sign": pair[4],
            },
            "targetCurrency": {
                "id": pair[5],
                "name": pair[7],
                "code": pair[6],
                "sign": pair[8],
            },
            "rate": float(pair[9]),
        }

        return formatted_pair
    
    def update_by_slug(self, base, target, rate):
        pair = ExchangeRatesModel().update_by_slug(base, target, rate)[0]

        formatted_pair = {
            "id": pair[0],
            "baseCurrency": {
                "id": pair[1],
                "name": pair[3],
                "code": pair[2],
                "sign": pair[4],
            },
            "targetCurrency": {
                "id": pair[5],
                "name": pair[7],
                "code": pair[6],
                "sign": pair[8],
            },
            "rate": float(pair[9]),
        }

        return formatted_pair
    
    def exchange(self, from_currency, to_currency, amount):
        pass
