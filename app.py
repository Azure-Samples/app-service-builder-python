"""Dependency-free learning sample, not a production HTTP server."""

import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from socketserver import TCPServer
from urllib.parse import urlsplit


class SampleHTTPServer(ThreadingHTTPServer):
    def server_bind(self):
        # HTTPServer's default bind performs reverse DNS for a display name.
        # This sample needs no DNS dependency; bind directly and use a fixed name.
        TCPServer.server_bind(self)
        self.server_name = "builder-python-sample"
        self.server_port = self.server_address[1]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/health":
            status, body = 200, "OK\n"
        elif path == "/":
            greeting = os.environ.get("SAMPLE_GREETING") or "Hello"
            status, body = 200, f"App Service Builder / python-web: {greeting}\n"
        else:
            status, body = 404, "Not found\n"
        content = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        # Do not print request URLs or environment variables.
        pass


if __name__ == "__main__":
    SampleHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
