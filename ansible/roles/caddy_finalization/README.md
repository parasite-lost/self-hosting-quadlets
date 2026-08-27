# Caddy Config Finalization

# Modularization

To keep the ansible project modular and flexible which backend services are
configured in the reverse proxy every backend service role adds its exposed port
in `caddy_pasta_port_map`; at the end of the playbook this `caddy_finalization`
role creates the respective port mapping for the caddy quadlet.

# mTLS

Since more elaborate TLS policies (for client authentication) cannot be
configured in the Caddyfile the Caddyfile config is adapted (using builtin caddy
functionality) to a json-based config and the required mTLS policy adjustment is
injected (see [script](scripts/add-remote-ip-matcher.py)) to render the final
caddy json-based config that will be used by caddy.

The Caddyfile config will also be deployed to the target host in
`{{ caddy_user_home }}/caddyfile_config` for reference, but not mounted into the caddy container.

An alternative would be to render a json config from the start using ansible and
jinja2 templates. This is explored and tested in the `caddy_json_config` role
and the accompanying playbook `caddy-render-json-testing.yaml`. While this may
be cleaner the Caddyfile syntax is more readable to humans.
