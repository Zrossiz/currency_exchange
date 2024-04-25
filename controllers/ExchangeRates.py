from services.ExchangeRates import ExchangeRatesService
import json


class ExchangeRatesController:

    def create(self, data):
        base_currency_code = data["baseCurrencyCode"]
        target_currency_code = data["targetCurrencyCode"]
        rate = data["rate"]
        new_pair = ExchangeRatesService().create(base_currency_code, target_currency_code, rate)

        response_json = json.dumps(new_pair)
        return response_json
