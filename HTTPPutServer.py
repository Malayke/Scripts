# ref: https://www.snip2code.com/Snippet/905666/Python-HTTP-PUT-test-server
import sys
import signal
from threading import Thread
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler



class PUTHandler(BaseHTTPRequestHandler):
    def do_PUT(self):
        length = int(self.headers['Content-Length'])
        content = self.rfile.read(length)
        self.send_response(200)
        with open(self.path[1:], "w") as f:
            f.write(content)


def run_on(port):
    print("Starting a HTTP PUT Server on {0} port {1} (http://{0}:{1}) ...".format(sys.argv[1], port))
    server_address = (sys.argv[1], port)
    httpd = HTTPServer(server_address, PUTHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:\n\tpython {0} localhost 1337".format(sys.argv[0]))
        sys.exit(1)
    ports = [int(arg) for arg in sys.argv[2:]]
    try:
        for port_number in ports:
            server = Thread(target=run_on, args=[port_number])
            server.daemon = True # Do not make us wait for you to exit
        server.start()
        signal.pause() # Wait for interrupt signal, e.g. KeyboardInterrupt
    except KeyboardInterrupt:
        print "\nPython HTTP PUT Server Stoped."
        sys.exit(1)
