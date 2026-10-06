#!/usr/bin/env python3
"""Local dev server with live reload. Not part of the published site.

Serves this folder like `python3 -m http.server`, but sends no-cache headers
and injects a small script into HTML pages that reloads the page whenever a
file in the folder changes.

    python3 dev.py [port]      # default 8000
"""
import os
import sys
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {'.git', '.claude', 'renders', '__pycache__'}
SNIPPET = b"""<script>(()=>{const es=new EventSource('/__reload');
es.addEventListener('change',()=>location.reload());})();</script>"""


def snapshot():
    """mtime of every watched file, keyed by path."""
    out = {}
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            p = os.path.join(d, f)
            try:
                out[p] = os.stat(p).st_mtime_ns
            except OSError:
                pass
    return out


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def do_GET(self):
        path = self.path.split('?', 1)[0].split('#', 1)[0]
        if path == '/__reload':
            return self.serve_events()
        fs = self.translate_path(path)
        if os.path.isdir(fs):
            if not path.endswith('/'):
                return super().do_GET()  # let the base class redirect
            fs = os.path.join(fs, 'index.html')
        if fs.endswith('.html') and os.path.isfile(fs):
            return self.serve_html(fs)
        return super().do_GET()

    def serve_html(self, fs):
        with open(fs, 'rb') as f:
            body = f.read()
        i = body.rfind(b'</body>')
        body = body[:i] + SNIPPET + body[i:] if i >= 0 else body + SNIPPET
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_events(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.end_headers()
        last = snapshot()
        try:
            while True:
                time.sleep(0.4)
                now = snapshot()
                if now != last:
                    last = now
                    self.wfile.write(b'event: change\ndata: 1\n\n')
                else:
                    self.wfile.write(b': ping\n\n')  # detects closed tabs
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass

    def log_message(self, fmt, *args):
        if '/__reload' not in self.path:
            super().log_message(fmt, *args)


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = ThreadingHTTPServer(('', port), partial(Handler, directory=ROOT))
    server.daemon_threads = True
    print(f'Serving {ROOT} with live reload at http://localhost:{port}/')
    server.serve_forever()
