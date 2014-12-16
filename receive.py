from http import server 

class MyHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Here's where all the complicated logic is done to generate HTML.
        # For clarity here, replace with a simple stand-in:
        html = "<html><p>hello world</p></html>"

        self.wfile.write(html.encode())

def run(server_class=server.HTTPServer, handler_class=MyHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()
