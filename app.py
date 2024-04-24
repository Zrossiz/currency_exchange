from http.server import BaseHTTPRequestHandler, HTTPServer
from Db import Db
import json


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        code = data["code"]
        name = data["name"]
        sign = data["sign"]

        Db().create_currency(code, name, sign)

        response_data = {
            "success": "true",
            "data": {
                "code": code,
                "name": name,
                "sign": sign
            }
        }

        response_json = json.dumps(response_data)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response_json.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=HTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()