# Immich

## Configuration

Run the following command to generate a client secret and its hash:

```
podman run --rm \
  authelia/authelia:latest \
  authelia crypto hash generate pbkdf2 \
    --variant sha512 \
    --random \
    --random.length 72 \
    --random.charset rfc3986
```


## First Time Setup (Account Provisioning)

1. create admin account (email does not need to exist) with
   **different name than admin account configured in authelia** - but remember
   login credentials for now
2. generate client secret

3. store client secret hash in `immich_client_secret_hash`
4. configure OIDC and enable login with OAuth:
  - `issuer_url`: `https://{{ authelia_subdomain }}.{{ host_maindomain }}/.well-known/openid-configuration`
  - `client_id`: `immich`
  - `client_secret`: plain text secret corresponding to hash `immich_client_secret_hash` (generate with `)
  - `scope`: `openid email profile immich_scope`
  - `id_token_signed_response_alg`: `RS256`
  - `userinfo_signed_response_alg`: `RS256`
  - `Role Claim`: `immich_role`
  - `Storage quota claim`: `immich_quota`
  - `Default storage quota (GiB)`: `0` (optional: default quota if not defiend via authelia)
  - **important**: do not toggle auto launch yet (to prevent a typo breaking authentication)!
  - save
5. log out
6. login with authelia admin account (OAuth) - if it doesn't work login
7. delete initial admin account
8. enable auto launch for OAuth login, disable Password login, save

References:

* https://www.authelia.com/integration/openid-connect/clients/immich/
* https://docs.immich.app/administration/oauth/

## Immich Mobile App + Authelia

There are two options:

1. selective basic auth

  * immich subdomain configured for mobile app users with `one_factor` policy (authelia)
  * in immich mobile app (before login: settings -> advanced -> proxy headers)
  * add header: `Authorization`
  * add value: `Basic ...` where `...` is base64 encoded `username:password`

2. optional mTLS:

  * immich subdomain configured with optional client TLS certificate (caddy) and `two_factor` authelia fallback
  * add client certificate to immich mobile app (before login: settings -> advanded -> client certificate)
  * with client certificate go directly to immich and use authelia only OAuth login
  * without client certificate login with authelia first, then go to immich and use authelia for OAuth (already logged in)
