# Caddy Config Finalization

# Modularization

To keep the ansible project modular and flexible which backend services are
configured in the reverse proxy every backend service role adds its exposed port
in `caddy_pasta_port_map`; at the end of the playbook this `caddy_finalization`
role creates the respective port mapping for the caddy quadlet.
