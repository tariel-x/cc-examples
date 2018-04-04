import requests
import sys
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO

# Register service

params = {"schemes":[{"in":True,"scheme":{'properties':{'random':{'type':'string'}},'type':'object'},"type":"json-schema"}],"service":{"name":"provider","address":{"endpoint": "http://localhost:8880"},"check_url":"http://localhost:8881/provider.json"}}
query = {'jsonrpc':'2.0','method':'registerContract','params':params,'id':1}
print(json.dumps(query))
r = requests.post(sys.argv[1], data=json.dumps(query))

print(r.content)
print("Register service")

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        print(body)
        self.wfile.write(response.getvalue())


httpd = HTTPServer(('0.0.0.0', 8880), SimpleHTTPRequestHandler)
httpd.serve_forever()