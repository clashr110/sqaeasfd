import os
from http.server import BaseHTTPRequestHandler, HTTPServer

clipboard_storage = ""

class ClipboardHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Любое устройство заходит по ссылке и получает скопированный текст"""
        global clipboard_storage
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(clipboard_storage.encode("utf-8"))

    def do_POST(self):
        """Принимает текст, который прислал твой ПК"""
        global clipboard_storage
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        clipboard_storage = post_data.decode("utf-8")

        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), ClipboardHandler)
    print(f"Сервер запущен на порту {port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")