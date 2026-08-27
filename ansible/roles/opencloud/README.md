# openCloud

* https://docs.opencloud.eu/docs/admin/
* https://docs.opencloud.eu/docs/admin/configuration/authentication-and-user-management/external-idp
* https://www.authelia.com/integration/openid-connect/clients/opencloud/

## Configuration

openCloud does not require a shared secret with authelia as it is configured as
a public client and is configured to automatically generate all its internal
secrets on first startup.

The only thing needed to configure is the mTLS certificate:

* `opencloud_root_ca`: path to mTLS root CA certificate to guard openCloud

## mTLS

openCloud seems to be connecting to itself, so guarding behind authelia does not
work without some exception policy in authelia.  openCloud can also not be
configured to use an mTLS certificate. Using an optional mTLS certificate breaks
openCloud desktop browsers as they rarely use certificates when they are
optional (openCloud becomes completely unusable).

What is needed is mTLS enforcement base on IP address: external IPs connecting
must use a mTLS certificate, local connection (openCloud to itself) do require
an mTLS certificate. This is solved by injecting a remote_ip matcher into the
json caddy configuration.
