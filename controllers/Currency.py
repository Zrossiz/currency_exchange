from services.Currency import CurrencyService
import json


class CurrencyController:

    def create(self, data):

        if not "code" in data:
            return json.dumps({
                "success": "false",
                "data": "indicate the currency code"
            })
        if not "name" in data:
            return json.dumps({
                "success": "false",
                "data": "indicate the currency name"
            })
        if not "sign" in data:
            return json.dumps({
                "success": "false",
                "data": "indicate the currency sign"
            })

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

    def get_currency_by_slug(self, slug):
        currency = CurrencyService().get_currency_by_slug(slug)
        response_json = json.dumps(currency)
        return response_json
