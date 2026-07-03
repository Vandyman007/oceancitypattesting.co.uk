#!/usr/bin/env python3
"""
Clean-URL static preview server for Ocean City PAT Testing.

WHY THIS EXISTS
    The site links with clean URLs (/services, /areas-covered/plymouth) but
    ships flat files (services.html, areas-covered/plymouth.html). The
    production host (Cloudflare Pages / Netlify) rewrites the clean URL to the
    flat file automatically. A plain `python3 -m http.server` does NOT — so
    every clean-URL link 404s locally and the site looks broken even though the
    links are perfectly correct.

    This server mimics the host so local navigation behaves exactly like
    production. ALWAYS preview with this, never with a bare static server.

USAGE
    python3 tools/serve.py            # http://localhost:8000
    python3 tools/serve.py 8787       # custom port

    The same resolve_path() logic backs `python3 tools/audit.py --live`, so the
    audit's link check and the preview server can never disagree.
"""
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import unquote, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resolve_path(url_path):
    """Map a request URL path to a file on disk using the host's clean-URL
    rules. Returns (abs_file_path, http_status) — status is 200 for a real
    page/asset, or 404 (serving 404.html) for anything that doesn't resolve.
    This is the SINGLE source of truth for how a URL becomes a file."""
    path = unquote(urlparse(url_path).path)
    parts = [p for p in path.split("/") if p not in ("", ".", "..")]
    rel = os.path.join(*parts) if parts else ""
    base = os.path.join(ROOT, rel)

    # 1. explicit directory request (/foo/) -> its index.html
    if path.endswith("/") and rel:
        idx = os.path.join(base, "index.html")
        if os.path.isfile(idx):
            return idx, 200
    # 2. site root
    if not rel:
        return os.path.join(ROOT, "index.html"), 200
    # 3. exact file on disk (assets + any *.html asked for directly)
    if os.path.isfile(base):
        return base, 200
    # 4. clean URL -> <path>.html
    if os.path.isfile(base + ".html"):
        return base + ".html", 200
    # 5. directory containing index.html
    idx = os.path.join(base, "index.html")
    if os.path.isfile(idx):
        return idx, 200
    # 6. host 404 fallback (matches _redirects: /* /404.html 404)
    return os.path.join(ROOT, "404.html"), 404


class CleanURLHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self._serve(head_only=False)

    def do_HEAD(self):
        self._serve(head_only=True)

    def _serve(self, head_only):
        file_path, status = resolve_path(self.path)
        if not os.path.isfile(file_path):
            self.send_error(404)
            return
        try:
            with open(file_path, "rb") as f:
                data = f.read()
        except OSError:
            self.send_error(404)
            return
        self.send_response(status)
        self.send_header("Content-Type", self.guess_type(file_path))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if not head_only:
            self.wfile.write(data)

    def log_message(self, fmt, *args):
        pass  # keep the preview quiet


def make_server(port):
    return HTTPServer(("127.0.0.1", port), CleanURLHandler)


def serve(port=8000):
    httpd = make_server(port)
    print(f"Ocean City PAT Testing preview (clean URLs) -> http://localhost:{port}/")
    print("Every clean-URL link resolves exactly as it will in production. Ctrl-C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")
        httpd.server_close()


if __name__ == "__main__":
    serve(int(sys.argv[1]) if len(sys.argv) > 1 else 8000)
