"""
Sambung Kata — Dev Server (multi-language)
Serves static files from the current folder + API endpoints to modify per-language word files.

Folder structure (root):
  index.html
  id/index.html
  id/wordsv1.json
  en/index.html
  en/wordsv1.json

Usage:
  python server.py
  Then open http://localhost:8000/

API (per language):
  POST /id/api/delete   {"word": "..." }  → remove word from id/wordsv1.json
  POST /id/api/add      {"word": "..." }  → add word (sorted) to id/wordsv1.json

  POST /en/api/delete   {"word": "..." }  → remove word from en/wordsv1.json
  POST /en/api/add      {"word": "..." }  → add word (sorted) to en/wordsv1.json
"""

import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LANGS = ("id", "en")
WORDS_FILENAME = "words.json"

# Cache per language for faster operations
words_cache = {lang: [] for lang in LANGS}


def _words_path(lang: str) -> str:
    return os.path.join(BASE_DIR, lang, WORDS_FILENAME)


def load_words(lang: str) -> None:
    path = _words_path(lang)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("word file must be a JSON array")
        # Normalize to lowercase strings
        words_cache[lang] = sorted({str(w).strip().lower() for w in data if str(w).strip()})
    except FileNotFoundError:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        words_cache[lang] = []
        save_words(lang)
    print(f"[server] Loaded {len(words_cache[lang]):,} words from {path}")


def save_words(lang: str) -> None:
    path = _words_path(lang)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(words_cache[lang], f, ensure_ascii=False)


def binary_search(arr, word: str) -> int:
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < word:
            lo = mid + 1
        else:
            hi = mid
    return lo


class SambungHandler(SimpleHTTPRequestHandler):
    # Serve static files as usual; only intercept API POSTs.

    def do_POST(self):
        path = urlparse(self.path).path

        # Expect: /<lang>/api/<action>
        parts = [p for p in path.split("/") if p]
        if len(parts) == 3 and parts[1] == "api":
            lang, _, action = parts
            if lang not in LANGS:
                return self._json_response(404, {"ok": False, "error": "Invalid language"})
            if action == "add":
                return self._handle_add(lang)
            if action == "delete":
                return self._handle_delete(lang)

        return self._json_response(404, {"ok": False, "error": "Not found"})

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def _json_response(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_delete(self, lang: str):
        try:
            body = self._read_body()
            word = str(body.get("word", "")).strip().lower()
            if not word:
                return self._json_response(400, {"ok": False, "error": "Missing 'word'"})

            arr = words_cache[lang]
            idx = binary_search(arr, word)
            if idx < len(arr) and arr[idx] == word:
                arr.pop(idx)
                save_words(lang)
                print(f"[server] ({lang}) Deleted '{word}' — {len(arr):,} words remaining")
                return self._json_response(200, {"ok": True, "total": len(arr)})

            return self._json_response(404, {"ok": False, "error": f"'{word}' not found"})
        except Exception as e:
            return self._json_response(500, {"ok": False, "error": str(e)})

    def _handle_add(self, lang: str):
        try:
            body = self._read_body()
            word = str(body.get("word", "")).strip().lower()
            if not word:
                return self._json_response(400, {"ok": False, "error": "Missing 'word'"})

            arr = words_cache[lang]
            idx = binary_search(arr, word)
            if idx < len(arr) and arr[idx] == word:
                return self._json_response(409, {"ok": False, "error": f"'{word}' already exists"})

            arr.insert(idx, word)
            save_words(lang)
            print(f"[server] ({lang}) Added '{word}' — {len(arr):,} words total")
            return self._json_response(200, {"ok": True, "total": len(arr)})
        except Exception as e:
            return self._json_response(500, {"ok": False, "error": str(e)})

    def log_message(self, format, *args):
        # Only log API calls or non-200 to reduce noise
        status = args[1] if len(args) > 1 else ""
        path = ""
        try:
            path = args[0].split()[1]
        except Exception:
            pass
        if "/api/" in path or str(status).startswith(("4", "5")):
            super().log_message(format, *args)


def main():
    os.chdir(BASE_DIR)
    for lang in LANGS:
        load_words(lang)

    server = HTTPServer(("", PORT), SambungHandler)
    print(f"[server] Running at http://localhost:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
