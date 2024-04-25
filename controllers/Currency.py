from services.Currency import CurrencyService
import json


class CurrencyController:

    def create(self, data):
        code = data["code"]
        full_name = data["name"]
        sign = data["sign"]
        new_currency = CurrencyService().create_currency(code, full_name, sign)

        response_json = json.dumps(new_currency)
        return response_json

    def get_all(self):
        currencies = CurrencyService().get_all()
        response_json = json.dumps(currencies)
        return response_json
