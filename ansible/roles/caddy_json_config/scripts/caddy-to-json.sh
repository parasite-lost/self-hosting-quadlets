#!/usr/bin/env bash

if [[ $# -lt 1 ]]; then
  echo "argument required: SRC_FILE"
  exit 1
fi

file=$(realpath "$1")
filename=$(basename "${file}")
folder=$(dirname "${file}")

podman run --rm -it \
  -v "${folder}":/work:ro,Z \
  -w /work \
  ghcr.io/caddybuilds/caddy-cloudflare \
  caddy adapt --config /work/"${filename}"
