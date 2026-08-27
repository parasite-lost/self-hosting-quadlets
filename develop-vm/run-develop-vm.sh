#!/usr/bin/env bash

if [[ $# -lt 1 ]]; then
  echo "Usage: $(basename "$0") QEMU_IMAGE" >&2
  exit 1
fi

image=$1

qemu-system-x86_64 \
  -m 4G \
  -smp 4 \
  -cpu host \
  -enable-kvm \
  -drive file="$image",if=virtio \
  -netdev user,id=n1,hostfwd=tcp::2222-:22,hostfwd=tcp::8025-:8025,hostfwd=tcp::8080-:80,hostfwd=tcp::8443-:443,hostfwd=udp::8443-:443 \
  -device virtio-net-pci,netdev=n1 \
  -monitor telnet::45454,server,nowait \
  -nographic \
  -serial mon:stdio
# to run VM completely headless with qemu console only:
# replace `-nographic -serial mon:stdio` with `-display none -serial null -monitor stdio`
