from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from controllers.Currency import CurrencyController
from controllers.ExchangeRates import ExchangeRatesController


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if (self.path == '/api/currency'):
            try:
                currencies = CurrencyController().get_all()
                if 'data' in currencies:
                    self.send_response(404)
                else:
                    self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(currencies.encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        
        if (self.path == '/api/exchange-rates'):
            try:
                exchange_pairs = ExchangeRatesController().get_all()
                if 'data' in exchange_pairs:
                    self.send_response(404)
                else:
                    self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(exchange_pairs.encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

        if self.path.startswith('/api/currency/'):
            try:
                slug = self.path.split('/')[-1].lower()
                currency = CurrencyController().get_currency_by_slug(slug)
                if len(slug) == 0:
                    self.send_response(400)
                elif 'data' in currency:
                    self.send_response(404)
                else:
                    self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(currency.encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        
        if self.path.startswith('/api/exchange-rates/'):
            slug = self.path.split('/')[-1].lower()
            pair = ExchangeRatesController().get_by_slug(slug)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(pair.encode('utf-8'))


    def do_POST(self):
        if (self.path == '/api/currency'):
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))

                new_currency = CurrencyController().create(data)
                data_message = json.loads(new_currency).get("data")
                if data_message == 'currency already exist':
                    self.send_response(409)
                elif data_message.startswith('indicate the'):
                    self.send_response(400)
                else:
                    self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(new_currency.encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

        if (self.path == '/api/exchange-rates'):
            try:
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
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

    def do_PATCH(self):
        if self.path.startswith('/api/exchange-rates/'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            slug = self.path.split('/')[-1].lower()
            pair = ExchangeRatesController().update_by_slug(slug, data)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(pair.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=HTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
