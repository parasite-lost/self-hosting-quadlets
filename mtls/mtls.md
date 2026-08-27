# mTLS Certificates for subdomain access control

Idea: every group of subdomains that should be accessible by a certain group of
people gets a unique root CA and client certificate pair; everyone that is
allowed to access the subdomain gets the client certificate. For example a
general purpose certificate pair for some shared subdomains (image sharing,
cloud storage, shared shopping list, etc.) and an admin certificate pair for
restricted subdomains (home assistant, cockpit, etc.).

## Script

Generate root CA and client certificate for `common.test.localhost` with a
validity of 10 years (validity in this setup is practically irrelevant as you
can just rotate root CA and client certificates whenever you feel like it):

```
./generate-mtls.py --target common.test.localhost --root-cn "Common root CA test.localhost" --client-cn "Common client test.localhost" --validity 3650
```

Note: currently the script only supports generating a root certificate (for the
reverse proxy) and a single client certificate that authorizes access to all subdomains
guarded by an mTLS policy configured with the root certificate. Multiple
additional client certificates can be generated manually.

## Manually:

1. create root key (EC)

```
openssl ecparam -name secp384r1 -genkey -out root@common.test.localhost.key
```

2. create root CA

  - days: validity time period
  - `/O=` organization (optional)
  - `/CN=` common name (required)
  - `pathlen:0` prevent intermediate CAs

```
openssl req -new -key root@common.test.localhost.key -x509 -nodes -days 3650 -out root@common.test.localhost.pem -subj "/CN=Common root CA test.localhost" -addext "basicConstraints=critical,CA:TRUE,pathlen:0"
```

3. create client key (EC)

```
openssl ecparam -name prime256v1 -genkey -out client@common.test.localhost.key
```

4. signing request for client cert

```
openssl req -new -key client@common.test.localhost.key -out client@common.test.localhost.csr -subj "/CN=Common client test.localhost" -addext "extendedKeyUsage = clientAuth"
```

5. sign client cert with root key/CA

```
openssl x509 -req -in client@common.test.localhost.csr -CA root@common.test.localhost.pem -CAkey root@common.test.localhost.key -CAcreateserial -out client@common.test.localhost.crt -days 365 -sha256 -copy_extensions=copyall
```

6. create client p12 certificate

```
openssl pkcs12 -export -out client@common.test.localhost.p12 -in client@common.test.localhost.crt -inkey client@common.test.localhost.key
```
