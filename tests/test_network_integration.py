import json
import socket
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from aidoc.checks import check_http, check_openai_compatible, check_tcp
from aidoc.model import CheckSpec


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = b'{"ok":true}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == "/v1/models":
            body = json.dumps(
                {"data": [{"id": "demo-model"}]}
            ).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        return


class NetworkIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(
            target=cls.server.serve_forever,
            daemon=True,
        )
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def test_real_local_http_tcp_and_openai_compatible_checks(self):
        tcp = CheckSpec(
            "tcp",
            "deployment",
            "tcp",
            True,
            {"host": "127.0.0.1", "port": self.port},
        )
        http = CheckSpec(
            "http",
            "deployment",
            "http",
            True,
            {
                "url": f"http://127.0.0.1:{self.port}/health",
                "accept_status": [200],
            },
        )
        model = CheckSpec(
            "model",
            "model",
            "openai-compatible",
            True,
            {
                "base_url": f"http://127.0.0.1:{self.port}/v1",
                "model": "demo-model",
            },
        )

        self.assertEqual(check_tcp(tcp).status, "PASS")
        self.assertEqual(check_http(http).status, "PASS")
        self.assertEqual(
            check_openai_compatible(model).status,
            "PASS",
        )


if __name__ == "__main__":
    unittest.main()
