#!/usr/bin/env bash

if [[ $# -lt 1 ]]; then
  echo "argument required: FILE"
  exit 1
fi

file=$(realpath "$1")
filename=$(basename  "${file}")
file_folder=$(dirname "${file}")
base_folder=$(dirname "${file_folder}")

TMPDIR=$(mktemp -d)

if [ ! -d "${TMPDIR}" ]; then
  echo "Failed to create temp directory"
  exit 1
fi

trap 'exit 1' HUP INT PIPE QUIT TERM
trap 'rm -rf "$TMPDIR"'  EXIT

podman run --rm -it \
  -v "${base_folder}/fakes/certs":/etc/caddy/certs:ro,Z \
  -v "${base_folder}/fakes/credentials":/run/credentials:ro,Z \
  -v "${TMPDIR}":/data/:rw,Z \
  -v "${file_folder}":/work:ro,Z \
  -w /work ghcr.io/caddybuilds/caddy-cloudflare \
  caddy validate --config /work/"${filename}"
