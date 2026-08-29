# Multi-User Rootless Podman Quadlet Web Service Setup

**WORK IN PROGRESS**

## Architecture & Design

* every service runs under a separate user (reverse proxy,
  authentication, backend services).
* every service is managed in a systemd user session (lingering user).
* every service is run inside a rootless podman container (optionally inside a
  pod).
* no service has access to the full host network.
* use systemd socket activation where suitable to ensure native network
  performance.
* inter-service communication (across user boundaries): TCP sockets:
  `PodmanArgs=--network=pasta:-T,9999,-T,1234` to map `127.0.0.1:9999` and
  `127.0.0.1:1234` into caddy container so caddy can proxy backend services
  exposing ports `127.0.0.1:9999` and `127.0.0.1:1234`. For security reasons no
  service should use host network and no service's port should be exposed on
  external host interface (except the reverse proxy's ports of course).
* every backend service is ideally guarded either by authelia or
  an [mTLS certificate](mtls/mtls.md).
* credentials and other sensitive data are encrypted at rest via systemd
  credentials (TPM encrypted), mounted into the service (automatically by
  systemd) and then mounted into the service's container as a volume mount

### Alternatives

Inter-service communication may (or may not) be possible using unix domain
sockets together with `systemd-socket-proxyd` to activate unix socket on one
user, proxy to other user's unix socket; while this would be more secure, it
most likely has worse performance due to the proxying and is more complex; plus,
most containerized services come documented for use with tcp sockets anyways.

Using unix domain sockets directly is most likely impossible due to podman
subuids/subgids which at least makes default unix permissions incompatible. It
may be feasible using ACLs, potentially requiring SELinux rules; but that's
where I stopped looking into this alternative.

Credentials could be provided using container secrets, particularly for
applications whose developers are hellbent on insecurely providing secrets via
environment variables; but I'll try to avoid such applications.

## Services

* [caddy](ansible/roles/caddy/README.md): reverse proxy
* [authelia](ansible/roles/authelia/README.md): SSO, OAuth2/OIDC
* [immich](ansible/roles/immich/README.md): image and video management
* [opencloud](ansible/roles/opencloud/README.md): generic cloud storage
* ...

## TODO:

* exploration of caddy config (json / adapt + inject): [caddy_json_config](ansible/roles/caddy_json_config/)
* filter groups for OIDC claims: https://www.authelia.com/integration/openid-connect/openid-connect-1.0-claims/
* run static website as separate user
* general ansible project cleanup
* reuse more tasks (create quadlet file, create systemd unit, ...)
* custom caddy image builds: https://caddy.community/t/how-to-guide-caddy-v2-cloudflare-dns-01-via-docker/8007
* add more services

## Development VM Setup

See [Development VM Setup](develop-vm/develop-vm.md)

## Ansible Setup

Deploy your ssh key to the target host before you start.

### Configuration

Add inventory and `host_vars` (optional: `group_vars`) outside the repository
(never commit secrets to a public repo!). A possible structure could be:

```
inventory/
├── inventory.yaml          # ansible inventory
├── group_vars/             # ansible looks here for group-specific variables
│   └── all/                # ansible looks here for variables for all hosts
│       ├── caddy.yaml      # caddy-specific variables for all hosts
│       └── authelia.yaml   # authelia-specific variables for all hosts
├── host_vars/              # ansible looks here for host-specific variables
│   ├── develop/            # contains variables for the host 'develop'
│   │   ├── caddy.yaml      # caddy-specific variables for the host 'develop'
│   │   └── authelia.yaml   # authelia-specific variables for the host 'develop'
│   └── webserver/          # contains variables for the host 'webserver'
└── files/                  # place for host-specific assets
    └── all/                # files for all hosts
        ├── authelia/       # (example) inventory-specific authelia assets
        │   ├── favicon.ico # (example) authelia favicon, reference with:
        │   └── logo.png    # (example) authelia logo, reference with:
        └── develop/        # files for the host 'develop'
```

`inventory.yaml`:

```yaml
development:
  hosts:
    develop:
      deploy_purpose: "development"
      ansible_user: "develop"
      host_maindomain: "test.localhost"
```

`authelia.yaml`:

```yaml
  authelia_logo: "{{ inventory_dir }}/files/all/authelia/logo.png"
  authelia_favicon: "{{ inventory_dir }}/files/all/authelia/favicon.ico"
```

Optional: create `ansible.cfg` and adjust general ansible parameters.

Run playbooks with `ansible-playbook my-playbook.yaml -i /path/to/inventory/inventory.yaml ...`

### Main Plays

Generally run them with `--limit`, e.g. `--limit develop` (guard to ensure
conscious decision to first deploy to development setup, test, then deploy to
production setup).

Initially run with `--tags validate` to perform some prechecks, mostly whether
all necessary variables are defined in the inventory (host_vars, group_vars).

Then run with `--check` or `--check --diff` to perform a dry-run.

* `basic-setup.yaml`: first time admin setup (install basic packages, disable
  password login)
* `production.yaml`: generic services only necessary/functional on production
  server (ddns, mdns, remote service)
* `web-hosting.yaml`: web services (caddy, authelia, immich, ...)

Several roles have a variable to force rewriting credentials; this is
particularly necessary when rotating credentials; for example to rewrite
authelia's credentials use `--extra-vars '{"authelia_refresh_credential": true}'`.
The reason for this is that systemd credential encryption is not idempotent
so if the credential already exists it is not written again to ensure the
ansible playbook is idempotent.

# (Un)Licensing

[UNLICENSE](UNLICENSE)
