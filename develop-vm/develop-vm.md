# Development VM Setup

## first time setup

1. download fedora server qemu image
2. resize to suitable size, e.g. to 15GB with `qemu-img resize fedora-server.qcow2 15G`
3. run VM with `./run-develop-vm.sh fedora-server.qcow2`
4. follow instructions for first time fedora server setup
5. resize volume/filesystem *inside* the vm (adjust device paths as needed):
   * `sudo pvresize /dev/vda4`
   * `sudo lvextend -r -l+100%FREE /dev/mapper/systemVG-LVRoot`
6. for convenience deploy your ssh key to the VM
7. add a suitable host entry in your `~/.ssh/config` to connect to the VM, e.g.

```
Host develop
  Hostname localhost
  User develop
  Port 2222
```

8. create an ansible inventory file for the development VM, e.g.:

```yaml
development:
  hosts:
    develop:
      ansible_user: "develop"
      host_maindomain: "test.localhost"
      deploy_purpose: "development"
```

## development deployment and testing

From the ansible directory run the playbook:

```bash
ansible-playbook web-hosting.yaml \
  -i ../../path/to/your/inventory.yaml \
  --limit develop \
  --tags validate
```

This will check if all required variables are defined.
Define all required variables in `host_vars/develop/*.yaml` or directly in the
inventory file (as above). All variables referencing secrets are documented in
the place where they are used how to generate suitable values.

Finally, run the playbook (use `--check` for a dry-run, and `--diff` to see more
information on changes):

```bash
ansible-playbook  web-hosting.yaml \
  -i ../../path/to/your/inventory.yaml \
  --limit develop
```

This will deploy a local-only test mail server (mailpit) reachable on your host
under http://localhost:8025/ for authentication flows when authelia is configured
accordingly:

```yaml
authelia_smtp_address: 'smtp://127.0.0.1:1025'
authelia_smtp_sender: 'Authelia Development <authelia@localhost>'
authelia_smtp_username: ''
authelia_smtp_password: ''
```

Run `sudo socat TCP-LISTEN:443,fork TCP:127.0.0.1:8443` to be able to access
https://SUBDOMAIN.test.localhost for any of your subdomains without messing
around with custom ports.

## VM control

Connect to qemu console: `telnet localhost 45454`
