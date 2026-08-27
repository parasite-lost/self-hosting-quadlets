# Remote Service Client Setup

1. on client generate unique ssh key for client {{ remote_service_client_admin }}
   user account
2. copy content of public ssh key into host variable `remote_service_ssh_key`
3. ensure the {{ remote_service_client_admin }} user account on the client
   machine is lingering with `sudo loginctl enable-linger {{remote_service_client_admin }}`
4. create, enable and start the following service on the client machine:

```
[Unit]
Description=Setup a secure reverse tunnel to {{ remote_service_subdomain }}.{{ host_maindomain }}
After=network.target

[Service]
ExecStart=/usr/bin/ssh -NT \
            -o ServerAliveInterval=60 \
            -o ExitOnForwardFailure=yes \
            -R {{ remote_service_port }}:localhost:22 \
            {{ remote_service_user_name }}@{{ remote_service_subdomain }}.{{ host_maindomain }}
RestartSec=5
Restart=always

[Install]
WantedBy=multi-user.target
```

# Remote SSH setup

1. on your own machine add the following host entry to `$HOME/.ssh/config`:

```
Host client
  Hostname localhost
  Port {{ remote_service_port }}
  User {{ remote_service_client_admin }}
  ProxyJump {{ host_maindomain }}
```

2. also have a config entry for {{ host_maindomain }}:

```
Host {{ host_maindomain }}
  User {{ ansible_user }}
  ...
```

3. you can now easily ssh directly to the client with `ssh client` whenever the
   client machine is online
