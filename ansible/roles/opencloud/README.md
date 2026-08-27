# OpenCloud

OpenCloud is a cloud storage solution. Accounts are automatically provisioned
via Authelia.

## Configuration

### OpenCloud

* https://docs.opencloud.eu/docs/admin/
* https://docs.opencloud.eu/docs/admin/configuration/authentication-and-user-management/external-idp
* https://www.authelia.com/integration/openid-connect/clients/opencloud/

OpenCloud does not require a shared secret with Authelia as it is configured as
a public client and will automatically generate all its internal secrets on
first startup.

The only thing needed to configure is the mTLS certificate:

* `opencloud_root_ca`: path to mTLS root CA certificate to guard OpenCloud

## mTLS

OpenCloud seems to be connecting to itself, so guarding behind Authelia does not
work without some exception policy in Authelia. OpenCloud itself can also not be
configured to use an mTLS certificate. Using an optional mTLS certificate breaks
OpenCloud desktop browsers as they rarely use certificates when they are
optional (OpenCloud becomes completely unusable).

What is needed is mTLS enforcement based on IP address: external IPs connecting
must use a mTLS certificate, local connection (OpenCloud to itself) do require
an mTLS certificate. This is solved by injecting a remote_ip matcher into the
json caddy configuration.
