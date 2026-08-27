#!/usr/bin/env python

import json
import os
import sys

def inject_remote_ip_matcher(input_data: str):
    """add `remote_ip` matcher to every tls connection policy in mode
    `require_and_verify` to allow connections on localhost without mTLS
    certificate"""
    try:
        config = json.loads(input_data)
    except json.JSONDecodeError as e:
        print(f"Invalid json: {e}", file=sys.stderr)
        sys.exit(os.EX_USAGE)

    try:
        servers = config["apps"]["http"]["servers"]
        server_names = servers.keys()
    except KeyError as e:
        print(f"Invalid json: {e}", file=sys.stderr)
        sys.exit(os.EX_USAGE)

    for server_name in server_names:
        current_server = servers[server_name]
        if "tls_connection_policies" in current_server:
            policies = current_server["tls_connection_policies"]
        else:
            policies = None
        if not isinstance(policies, list) or len(policies) == 0:
            continue
        for policy in policies:
            try:
                if policy["client_authentication"]["mode"] == "require_and_verify":
                    policy["match"]["remote_ip"] = { "not_ranges": ["127.0.0.0/8", "::1/128"] }
            except KeyError:
                continue

    return config

def main():
    """Read caddy json config from stdin, inject `remote_ip` matcher snippet, write to stdout"""
    try:
        input_data = sys.stdin.read()
    except OSError as e:
        print(f"Failed to read from stdin: {e}", file=sys.stderr)
        sys.exit(os.EX_OSERR)

    modified_config = inject_remote_ip_matcher(input_data)
    print(json.dumps(modified_config, indent=2))

if __name__ == "__main__":
    main()
