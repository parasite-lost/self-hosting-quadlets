# Caddy

Documentation: https://caddyserver.com/docs/

Configuration is done via modular Caddyfile.

## Configuration

* `caddy_dns_provider`: currently supported: `cloudflare` or `localhost`
* `caddy_cloudflare_acme_api_token`: in case of `cloudflare` dns provider the required cloudflare API token
* `caddy_container_image`: container image name, e.g. `ghcr.io/caddybuilds/caddy-cloudflare:latest`
* `caddy_root_certificates`: list of mTLS root CA certificates for mTLS guarded subdomains

## Modular Caddyfile, mTLS

Some finalization steps are necessary after all backend service roles have been
run: [caddy_finalization](../caddy_finalization/README.md).

Reasons:

* Caddyfile does not support elaborate mTLS policies and needs to be converted
  to json first (builtin caddy functionality).
* To keep the configuration modular additional data on the backend services'
  ports are needed before the configuration for the caddy container is complete
