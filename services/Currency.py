from models.Currency import CurrencyModel


class CurrencyService:

    def create_currency(self, code, full_name, sign):
        CurrencyModel().create_currency(code, full_name, sign)

        response_data = {
            "success": "true",
            "data": {
                "code": code,
                "name": full_name,
                "sign": sign
            }
        }

        return response_data
