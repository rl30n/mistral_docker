from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import parse_qs
from mistral_repsol_faq_qa_loop_simpl import main  # Cambiar si no es main

class SimpleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')
        data = parse_qs(body)
        pregunta = data.get("pregunta", [""])[0]

        respuesta = main(pregunta)  # ⚠️ Cambiar si la función es diferente

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"respuesta": respuesta}).encode('utf-8'))

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("web/index.html", "rb") as f:
                self.wfile.write(f.read())

if __name__ == "__main__":
    print("Servidor corriendo en http://localhost:8000")
    HTTPServer(("0.0.0.0", 8000), SimpleHandler).serve_forever()
