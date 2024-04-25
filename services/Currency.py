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


    def get_currency_by_slug(self, slug):
        currency = CurrencyModel().get_by_slug(slug)
        if currency:
            response_data = {
                "id": currency[0],
                "name": currency[1],
                "code": currency[2],
                "sign": currency[3]
            }

            return response_data
        else:
            response_data = {
                "success": "false",
                "data": "not found"
            }
            return response_data


    def get_all(self):
        currencies_sql_arr = CurrencyModel().get_all()

        formatted_sql = []

        for i in range(len(currencies_sql_arr)):
            current_currency = currencies_sql_arr[i]

            currency_object = {
                "id": current_currency[0],
                "name": current_currency[1],
                "code": current_currency[2],
                "sign": current_currency[3]
            }

            formatted_sql.append(currency_object)

        return formatted_sql
