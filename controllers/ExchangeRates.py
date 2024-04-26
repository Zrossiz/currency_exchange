from services.ExchangeRates import ExchangeRatesService
import json


class ExchangeRatesController:

    def create(self, data):

        if not "baseCurrencyCode" in data:
            return json.dumps({
                "success": "false",
                "data": "indicate the currency baseCurrencyCode"
            })
        if not "targetCurrencyCode" in data:
            return json.dumps({
                "success": "false",
                "data": "indicate the currency targetCurrencyCode"
            })
        if not "rate" in data:
            return json.dumps({
                "success": "false",
                "data": "indicate the currency rate"
            })

        base_currency_code = data["baseCurrencyCode"]
        target_currency_code = data["targetCurrencyCode"]
        rate = data["rate"]
        new_pair = ExchangeRatesService().create(base_currency_code, target_currency_code, rate)

        response_json = json.dumps(new_pair)
        return response_json

    def get_all(self):
        exchange_pairs = ExchangeRatesService().get_all()
        if len(exchange_pairs) == 0:
            response_json = {
                "success": "false",
                "data": "not found"
            }
            return json.dumps(response_json)
        response_json = json.dumps(exchange_pairs)
        return response_json
