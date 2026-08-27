# Authelia

## Configuration And Secure Parameters

Authelia needs several cryptographic paramers and provides tooling to generate them:

* https://www.authelia.com/configuration/methods/secrets/
* https://www.authelia.com/reference/guides/generating-secure-values/

The secrets provided will be encrypted as systemd credentials on the server
and mounted into the container securely:

* `authelia_storage_encryption_key`:
  - content of `AUTHELIA_STORAGE_ENCRYPTION_KEY_FILE`
  - `podman run --rm authelia/authelia:latest authelia crypto rand --length 64 --charset alphanumeric`
* `authelia_storage_password`:
  - content of `AUTHELIA_STORAGE_POSTGRES_PASSWORD_FILE`
* `authelia_session_secret`:
  - content of `AUTHELIA_SESSION_SECRET_FILE`
  - `podman run --rm authelia/authelia:latest authelia crypto rand --length 64 --charset alphanumeric`
* `authelia_jwt_secret`:
  - content of `AUTHELIA_IDENTITY_VALIDATION_RESET_PASSWORD_JWT_SECRET_FILE`
  - `podman run --rm authelia/authelia:latest authelia crypto rand --length 64 --charset alphanumeric`
* authelia_oidc_hmac_secret:
  - content of `AUTHELIA_IDENTITY_PROVIDERS_OIDC_HMAC_SECRET_FILE`
  - podman run --rm authelia/authelia:latest authelia crypto rand --length 64 --charset alphanumeric
* `authelia_oidc_jwk_key_file`:
  - path to key file, e.g. `"{{ inventory_dir }}/files/<host>/authelia/my-private-key.pem`
  - used for `identity_providers.oidc.jwks.key`
  - `podman run --rm -u "$(id -u):$(id -g)" -v "$(pwd)":/keys:rw,z authelia/authelia:latest authelia crypto pair rsa generate --directory /keys --file.private-key my-private-key.pem --file.public-key my-public-key.pem`
* `authelia_user_database`: path to file-based user database

## User Database

`authelia_user_database`: You need to provide a user database containing user
data including password hashes.
Below is an example with dummy passwords (DO NOT USE THESE IN PRODUCTION!).

To generate a password hash run
`podman run --rm -it authelia/authelia:latest authelia crypto hash generate argon2`,
see also https://www.authelia.com/reference/guides/passwords/#passwords.

```yaml
users:
  administrator:
    # test123
    password: $argon2id$v=19$m=65536,t=3,p=4$9Q5+MmDX4sB1GCqM8qZXrA$FP95xUsbV9JQUua/q0wAu58nzasOnNUsAQHlc3T4ADw
    displayname: Administrator
    email: admin@example.com
    groups:
      - admin
      - dev
    # custom attributes for immich account provisioning
    extra:
      immich_quota: "0"
      immich_role: admin
  test_user:
    # test123
    password: $argon2id$v=19$m=65536,t=3,p=4$9Q5+MmDX4sB1GCqM8qZXrA$FP95xUsbV9JQUua/q0wAu58nzasOnNUsAQHlc3T4ADw
    displayname: Test User
    email: user@example.com
    groups:
      - user
      - owner
    # custom attributes for immich account provisioning
    extra:
      immich_quota: "10"
      immich_role: user
```

## Optional configuration

### Theming

* `authelia_logo`: path to a png used as a logo on the authelia login page
* `authelia_favicon`: path to favicon used for authelia webpage

### Email templates

See: https://www.authelia.com/reference/guides/notification-templates/

* `authelia_event_html_template`: path to html template for Event emails
* `authelia_event_txt_template`: path to txt template for Event emails
* `authelia_otc_html_template`: path to html template for IdentityVerificationOTC emails
* `authelia_otc_txt_template`: path to txt template for IdentityVerificationOTC emails

## OIDC

https://www.authelia.com/integration/openid-connect/introduction/
https://www.authelia.com/integration/openid-connect/openid-connect-1.0-claims

Client configurations: https://www.authelia.com/integration/openid-connect/clients/
