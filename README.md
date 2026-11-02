# Minimal Domain Parking

One lightweight HTTP server for up to 999 domains. No third-party Python packages.

## Start

```sh
cp .env.example .env
# Edit .env: set EMAIL_CONTACT and DOMAIN1...DOMAIN999

docker compose up -d --build
```

Test locally:

```sh
curl -H 'Host: example.com' http://localhost:8080/
curl -H 'Host: example.com' http://localhost:8080/robots.txt
curl -H 'Host: example.com' http://localhost:8080/sitemap.xml
```

## Deployment

- Point the DNS records of your domains to your server.
- Put the container behind an HTTPS reverse proxy that forwards the original `Host` header to port `8080`. The canonical URLs and sitemap use HTTPS.
- `DOMAIN1` through `DOMAIN999` are supported; only defined entries are enabled. Add `www.example.com` explicitly if needed.
- Unknown domains and unknown paths return HTTP 404.
- The page exposes basic metadata and allows search engine crawling, but actual indexing is up to each search engine.
