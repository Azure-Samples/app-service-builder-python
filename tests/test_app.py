import os
import threading
import unittest
from http.client import HTTPConnection
from unittest.mock import patch

from app import Handler, SampleHTTPServer


class HTTPTests(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(os.environ, {}, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)
        with patch("socket.getfqdn", side_effect=AssertionError("Unexpected DNS lookup")):
            self.server = SampleHTTPServer(("127.0.0.1", 0), Handler)
        self.addCleanup(self.server.server_close)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop_server)

    def stop_server(self):
        self.server.shutdown()
        self.thread.join(timeout=5)
        self.assertFalse(self.thread.is_alive(), "Sample server did not stop")

    def assert_response(self, path, status, body):
        connection = HTTPConnection(*self.server.server_address, timeout=5)
        try:
            connection.request("GET", path)
            response = connection.getresponse()
            content = response.read()
            self.assertEqual(response.status, status)
            self.assertEqual(content, body.encode("utf-8"))
            self.assertEqual(response.getheader("Content-Length"), str(len(content)))
            self.assertEqual(
                response.getheader("Content-Type"), "text/plain; charset=utf-8"
            )
        finally:
            connection.close()

    def test_default_greeting(self):
        self.assert_response("/", 200, "App Service Builder / python-web: Hello\n")

    def test_health(self):
        self.assert_response("/health", 200, "OK\n")

    def test_unknown_path(self):
        self.assert_response("/not-found", 404, "Not found\n")

    def test_public_greeting(self):
        os.environ["SAMPLE_GREETING"] = "Welcome"
        self.assert_response("/", 200, "App Service Builder / python-web: Welcome\n")

    def test_empty_greeting_uses_default(self):
        os.environ["SAMPLE_GREETING"] = ""
        self.assert_response("/", 200, "App Service Builder / python-web: Hello\n")

    def test_query_does_not_change_route(self):
        self.assert_response("/health?check=1", 200, "OK\n")

    def test_bind_does_not_require_reverse_dns(self):
        self.assertEqual(self.server.server_name, "builder-python-sample")
        self.assertEqual(self.server.server_port, self.server.server_address[1])


if __name__ == "__main__":
    unittest.main()
