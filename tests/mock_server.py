"""
Mock OTA Backend Server for testing Edge Agent
Member B ke actual backend se pehle, yeh server
locally test karne ke liye use hoga.

Run: python mock_server.py
Port: http://localhost:8000
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import hashlib
import base64
import json
import os

FIRMWARE_CONTENT = b"MOCK_FIRMWARE_v1.0.0_INFOTACT_OTA_2026"
FIRMWARE_HASH = hashlib.sha256(FIRMWARE_CONTENT).hexdigest()

print(f"Mock server starting...")
print(f"Firmware hash: {FIRMWARE_HASH}")


class OTAHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        # Firmware binary download endpoint
        if self.path.startswith("/firmware/download/"):
            version = self.path.split("/")[-1]
            print(f"[Server] Firmware download request for v{version}")

            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.end_headers()
            self.wfile.write(FIRMWARE_CONTENT)

        # Signature endpoint
        elif self.path.startswith("/firmware/signature/"):
            version = self.path.split("/")[-1]
            print(f"[Server] Signature request for v{version}")

            response = {
                "version": version,
                "sha256_hash": FIRMWARE_HASH,
                "signature": base64.b64encode(b"MOCK_SIGNATURE").decode()
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")

    def log_message(self, format, *args):
        pass  # Default logs band karo


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), OTAHandler)
    print(f"Mock OTA Server running at http://localhost:8000")
    print(f"Press Ctrl+C to stop")
    server.serve_forever()