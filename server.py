"""
Sambung Kata — Dev Server
Serves static files + API endpoints to modify words.json on disk.

Usage:  python server.py
        Then open http://localhost:8000

API:
  POST /api/delete   {"word": "atam"}       → remove word from words.json
  POST /api/add      {"word": "newword"}     → add word to words.json (sorted)
"""

import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

WORDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "words.json")
PORT = 8000

# Keep words in memory for fast operations
words_cache = []


def load_words():
    global words_cache
    with open(WORDS_FILE, "r", encoding="utf-8") as f:
        words_cache = json.load(f)
    print(f"[server] Loaded {len(words_cache):,} words from {WORDS_FILE}")


def save_words():
    with open(WORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(words_cache, f, ensure_ascii=False)


def binary_search(arr, word):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < word:
            lo = mid + 1
        else:
            hi = mid
    return lo


class SambungKataHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        path = urlparse(self.path).path

        if path == "/api/delete":
            self._handle_delete()
        elif path == "/api/add":
            self._handle_add()
        else:
            self._json_response(404, {"ok": False, "error": "Not found"})

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def _json_response(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_delete(self):
        global words_cache
        try:
            body = self._read_body()
            word = body.get("word", "").strip().lower()
            if not word:
                self._json_response(400, {"ok": False, "error": "Missing 'word'"})
                return

            idx = binary_search(words_cache, word)
            if idx < len(words_cache) and words_cache[idx] == word:
                words_cache.pop(idx)
                save_words()
                print(
                    f"[server] Deleted '{word}' — {len(words_cache):,} words remaining"
                )
                self._json_response(200, {"ok": True, "total": len(words_cache)})
            else:
                self._json_response(
                    404, {"ok": False, "error": f"'{word}' not found in database"}
                )
        except Exception as e:
            self._json_response(500, {"ok": False, "error": str(e)})

    def _handle_add(self):
        global words_cache
        try:
            body = self._read_body()
            word = body.get("word", "").strip().lower()
            if not word:
                self._json_response(400, {"ok": False, "error": "Missing 'word'"})
                return

            idx = binary_search(words_cache, word)
            if idx < len(words_cache) and words_cache[idx] == word:
                self._json_response(
                    409, {"ok": False, "error": f"'{word}' already exists"}
                )
                return

            words_cache.insert(idx, word)
            save_words()
            print(f"[server] Added '{word}' — {len(words_cache):,} words total")
            self._json_response(200, {"ok": True, "total": len(words_cache)})
        except Exception as e:
            self._json_response(500, {"ok": False, "error": str(e)})

    def log_message(self, format, *args):
        # Only log non-200 or API calls, skip static file noise
        status = args[1] if len(args) > 1 else ""
        path = args[0].split()[1] if args and " " in str(args[0]) else ""
        if path.startswith("/api") or str(status).startswith(("4", "5")):
            super().log_message(format, *args)


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    load_words()

    server = HTTPServer(("", PORT), SambungKataHandler)
    print(f"[server] Sambung Kata running at http://localhost:{PORT}")
    print("[server] Press Ctrl+C to stop\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[server] Shutting down...")
        server.server_close()


if __name__ == "__main__":
    main()
