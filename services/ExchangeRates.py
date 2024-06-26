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
        pair = ExchangeRatesModel().get_by_slug(base, target)
        if len(pair) >= 1:
            formatted_pair = {
                "id": pair[0][0],
                "baseCurrency": {
                    "id": pair[0][1],
                    "name": pair[0][3],
                    "code": pair[0][2],
                    "sign": pair[0][4],
                },
                "targetCurrency": {
                    "id": pair[0][5],
                    "name": pair[0][7],
                    "code": pair[0][6],
                    "sign": pair[0][8],
                },
                "rate": float(pair[0][9]),
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
        pair = ExchangeRatesService().get_by_slug(base=from_currency, target=to_currency)
        if pair:
            pair["amount"] = int(amount)
            pair["convertedAmount"] = pair["amount"] * pair["rate"]
            return pair
        
        reverse_pair = ExchangeRatesService().get_by_slug(base=to_currency, target=from_currency)
        if reverse_pair:
            reverse_pair["rate"] = 1 / float(reverse_pair["rate"])
            reverse_pair["amount"] = int(amount)
            reverse_pair["convertedAmount"] = reverse_pair["amount"] * reverse_pair["rate"]
            return reverse_pair
        
        from_currency_to_usd = ExchangeRatesService().get_by_slug(base=from_currency, target='usd')
        from_usd_to_currency = ExchangeRatesService().get_by_slug(base='usd', target=to_currency)
        if from_currency_to_usd:
            amount_in_usd = int(amount) * float(from_currency_to_usd['rate'])
            print('Amount usd: ', amount_in_usd)
            amount_in_to_currency = amount_in_usd * float(from_usd_to_currency['rate'])
            result = {
                "baseCurrency": from_currency_to_usd["baseCurrency"],
                "targetCurrency": from_usd_to_currency["targetCurrency"],
                "amount": int(amount_in_to_currency)
            }
            return result