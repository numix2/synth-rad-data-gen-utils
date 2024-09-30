"""
This is an example for how to recieve the JSON object sent by the sensor.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json

ADDR = "localhost"
PORT = 8000

class SensorRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers['Content-length'])
        data = self.rfile.read1(length)
        json_data = json.loads(data)
        print(json_data)
        self.send_response(200, "OK")
        self.end_headers()
httpd = HTTPServer((ADDR, PORT), SensorRequestHandler)
httpd.serve_forever()
