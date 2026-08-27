# Caddy

Documentation: https://caddyserver.com/docs/

Configuration is done via modular Caddyfile.

Configuration:

* `caddy_dns_provider`: currently supported: `cloudflare` or `localhost`
* `caddy_cloudflare_acme_api_token`: in case of `cloudflare` dns provider the required cloudflare API token
* `caddy_container_image`: container image name, e.g. `ghcr.io/caddybuilds/caddy-cloudflare:latest`
* `caddy_root_certificates`: list of mTLS root CA certificates for mTLS guarded subdomains
