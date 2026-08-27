# Opencloud

* https://docs.opencloud.eu/docs/admin/
* https://docs.opencloud.eu/docs/admin/configuration/authentication-and-user-management/external-idp
* https://www.authelia.com/integration/openid-connect/clients/opencloud/

TODO: get it to work (with mTLS):

opencloud seems to be connecting to itself, so guarding behind authelia or mTLS
certificate does not work as opencloud cannot be easily configured to work with
authelia/mTLS. Optional mTLS certificate does not work as desktop browsers
rarely use certificates when they are optional (opencloud becomes unusable).
What is needed is the following: mTLS is enforced unless the connection is local -
unfortunately this is not supported by Caddyfiles but only by json caddy
configuration. Options:

1. render json config using ansible and jinja2 templates
2. or keep Caddyfile, adapt to json, inject remote_ip matcher into tls policy of json, deploy json
