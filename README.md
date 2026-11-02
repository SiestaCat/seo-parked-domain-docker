# Minimal Domain Parking

A lightweight HTTP server that shows a domain-for-sale page for any domain whose HTTP request reaches the service. No third-party Python packages or domain allowlist.

## Start

```sh
cp .env.example .env
# Edit .env and set EMAIL_CONTACT

docker compose up -d --build
```

`.env`:

```dotenv
EMAIL_CONTACT=contact@example.com
```

Test locally:

```sh
curl -H 'Host: example.com' http://localhost:8080/
curl -H 'Host: another-domain.com' http://localhost:8080/
curl -H 'Host: example.com' http://localhost:8080/robots.txt
curl -H 'Host: example.com' http://localhost:8080/sitemap.xml
```

## Deployment

- Point each domain's DNS `A`/`AAAA` record to the server (or to the reverse proxy in front of it).
- Configure the HTTPS reverse proxy to accept all intended domains and forward the original `Host` header to port `8080`.
- No `DOMAIN` environment variables are needed. Each request uses its `Host` header to display the domain name and generate its canonical URL and sitemap.
- Unknown paths and malformed `Host` headers return HTTP 404.
- The page includes basic SEO metadata and allows crawling; search engines decide whether to index it.
- The service cannot verify DNS ownership: it answers any valid `Host` header that reaches it. Configure host restrictions at the reverse proxy if needed.
