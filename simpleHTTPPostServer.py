# python -m SimpleHTTPPutServer 8080
# From: https://blog.anvileight.com/posts/simple-python-http-server/
# From: https://stackabuse.com/serving-files-with-pythons-simplehttpserver-module/
from http.server import HTTPServer, SimpleHTTPRequestHandler
import http.server
import socketserver

class MyHttpRequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print(body)
        self.send_response(200)
        self.end_headers()
        with open('index.html','r') as f:
            read_data = f.read()
        self.wfile.write(bytes(read_data, 'utf-8'))

# Create an object of the above class
handler_object = MyHttpRequestHandler

# httpd = SimpleHTTPServer(('localhost', 8000), handler_object)
# httpd.serve_forever()
PORT = 8000
with socketserver.TCPServer(("", PORT), handler_object) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()