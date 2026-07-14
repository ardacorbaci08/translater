#!/usr/bin/env python3
"""Web server for the English word lookup tool."""

import json
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from translator import get_turkish_meaning, get_word_data, get_tatoeba_sentences


class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # API endpoint for word search
        if path == "/api/search":
            word = query.get("word", [None])[0]
            if not word:
                self.send_json({"error": "Missing 'word' parameter"}, 400)
                return

            try:
                # Get all three data sources
                translation = get_turkish_meaning(word)
                definitions, examples = get_word_data(word)

                # Backfill examples from Tatoeba if needed
                if len(examples) < 3:
                    tatoeba_sentences = get_tatoeba_sentences(word)
                    for sentence in tatoeba_sentences:
                        if sentence not in examples:
                            examples.append(sentence)
                        if len(examples) >= 3:
                            break

                response = {
                    "word": word,
                    "translation": translation or "(bulunamadi)",
                    "definitions": definitions[:5] if definitions else [],
                    "examples": examples[:3] if examples else [],
                }
                self.send_json(response, 200)
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        # Serve index.html for root
        if path == "/":
            self.path = "/index.html"

        # Serve static files (HTML, CSS, JS)
        try:
            super().do_GET()
        except Exception as e:
            self.send_json({"error": str(e)}, 500)

    def send_json(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")


if __name__ == "__main__":
    PORT = 8000
    server = HTTPServer(("localhost", PORT), RequestHandler)
    print(f"Server running at http://localhost:{PORT}")
    print(f"Open your browser to http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()
