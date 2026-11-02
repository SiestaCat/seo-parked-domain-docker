import html
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import quote

EMAIL_CONTACT = os.getenv("EMAIL_CONTACT", "").strip()
DOMAINS = {
    value.strip().lower().rstrip(".")
    for i in range(1, 1000)
    if (value := os.getenv(f"DOMAIN{i}", ""))
}

if not EMAIL_CONTACT or not DOMAINS:
    raise SystemExit("Set EMAIL_CONTACT and at least one DOMAIN1...DOMAIN999")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.respond()

    def do_HEAD(self):
        self.respond(head_only=True)

    def respond(self, head_only=False):
        domain = self.headers.get("Host", "").split(":", 1)[0].lower().rstrip(".")
        if domain not in DOMAINS:
            self.send_error(404)
            return

        path = self.path.split("?", 1)[0]
        if path == "/":
            name = html.escape(domain)
            email = html.escape(EMAIL_CONTACT, quote=True)
            subject = quote(f"Inquiry about {domain}")
            body = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{name} — Domain for Sale</title>
  <meta name="description" content="{name} is available for purchase. Contact us to inquire about this domain.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://{name}/">
  <meta property="og:title" content="{name} — Domain for Sale">
  <meta property="og:description" content="This domain is available for purchase.">
  <meta property="og:url" content="https://{name}/">
  <style>
    body {{ margin: 0; min-height: 100vh; display: grid; place-items: center; background: #f0f0f2; color: #252525; font: 16px/1.6 system-ui, sans-serif; }}
    main {{ box-sizing: border-box; width: min(600px, calc(100% - 32px)); padding: clamp(28px, 6vw, 48px); background: white; border-radius: 12px; }}
    h1 {{ margin: 0 0 12px; font-size: clamp(24px, 5vw, 32px); line-height: 1.2; overflow-wrap: anywhere; }}
    p {{ margin: 0 0 20px; color: #555; }}
    a {{ color: #1769aa; overflow-wrap: anywhere; }}
    a:hover {{ text-decoration: none; }}
  </style>
</head>
<body>
  <main>
    <h1>{name} is for sale</h1>
    <p>Interested in buying this domain? Get in touch to discuss an offer.</p>
    <a href="mailto:{email}?subject={subject}">Contact: {email}</a>
  </main>
</body>
</html>
"""
            content_type = "text/html; charset=utf-8"
        elif path == "/robots.txt":
            body = f"User-agent: *\nAllow: /\nSitemap: https://{domain}/sitemap.xml\n"
            content_type = "text/plain; charset=utf-8"
        elif path == "/sitemap.xml":
            body = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://{domain}/</loc></url></urlset>\n'
            content_type = "application/xml; charset=utf-8"
        else:
            self.send_error(404)
            return

        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        if not head_only:
            self.wfile.write(data)


ThreadingHTTPServer(("0.0.0.0", int(os.getenv("PORT", "8080"))), Handler).serve_forever()
