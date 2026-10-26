# Caddy

Documentation: https://caddyserver.com/docs/

Configuration is done via modular Caddyfile.

## Configuration

* `caddy_dns_provider`: currently supported: `cloudflare` or `localhost`
* `caddy_cloudflare_acme_api_token`: in case of `cloudflare` dns provider the required cloudflare API token
* `caddy_version`: tag of the official caddy base images, default `2`
* `caddy_dns_plugin_version`: plugin version, e.g. `v0.2.4`, defaults to latest
* `caddy_image_rebuild_on_calendar`: systemd `OnCalendar=` of the regular image
  rebuild, default `Sun *-*-* 21:00`
* `caddy_root_certificates`: list of mTLS root CA certificates for mTLS guarded subdomains

## Container image

The image is built on the target host from the official caddy image with
`xcaddy` (`caddy.build` and `caddy-build.service`).

Updates: `caddy-image-rebuild.timer` rebuilds the image (pulling newer base
images), `podman-auto-update.timer` restarts caddy with the new image
(`AutoUpdate=local`, rolls back if caddy fails to start).

Manual update:

```
systemctl --user start caddy-image-rebuild.service
podman auto-update
```

## Modular Caddyfile, mTLS

Some finalization steps are necessary after all backend service roles have been
run: [caddy_finalization](../caddy_finalization/README.md).

Reason: To keep the configuration modular additional data on the backend
services' ports are needed before the configuration for the caddy container is
complete.
