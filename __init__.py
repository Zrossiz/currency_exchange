from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from controllers.Currency import CurrencyController
from controllers.ExchangeRates import ExchangeRatesController


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if (self.path == '/api/currency'):
            currencies = CurrencyController().get_all()
            if 'data' in currencies:
                self.send_response(404)
            else:
                self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(currencies.encode('utf-8'))

        if self.path.startswith('/api/currency/'):
            slug = self.path.split('/')[-1].lower()
            currency = CurrencyController().get_currency_by_slug(slug)
            if 'data' in currency:
                self.send_response(404)
            else:
                self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(currency.encode('utf-8'))

    def do_POST(self):
        if (self.path == '/api/currency'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            new_currency = CurrencyController().create(data)

            if 'data' in new_currency:
                self.send_response(400)
            else:
                self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(new_currency.encode('utf-8'))

        if (self.path == '/api/exchange-rates'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            new_pair = ExchangeRatesController().create(data)

            if 'data' in new_pair:
                self.send_response(400)
            else:
                self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(new_pair.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=HTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
