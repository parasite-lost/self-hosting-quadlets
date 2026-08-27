#!/usr/bin/env bash

if [[ $# -lt 2 ]]; then
  echo "arguments required: FILE FILE"
  exit 1
fi

json1=$1
json2=$2

# for comparison to work:
# - sort keys in all dictionaries
# - sort routes list by host (sni)
diff \
  <( \
    jq --sort-keys '.apps.http.servers.srv1.routes|=sort_by(.match[0].host)' "${json1}" \
  ) \
  <( \
    jq --sort-keys '.apps.http.servers.srv1.routes|=sort_by(.match[0].host)' "${json2}" \
  )
