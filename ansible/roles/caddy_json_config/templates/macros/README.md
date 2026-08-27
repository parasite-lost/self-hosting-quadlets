# Caddyfile -> json

## Order of directives

The (implicit) directive order of Caddyfile needs to be respected when writing a
json config

https://caddyserver.com/docs/caddyfile/directives#directive-order

1. `header`
2. `forward_auth`
3. `encode`
4. `reverse_proxy`
