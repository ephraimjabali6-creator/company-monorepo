#!/usr/bin/env bash
set -euo pipefail

# Wait for backend health endpoint and then call /plan
MAX_WAIT=60
COUNT=0
until [ $COUNT -ge $MAX_WAIT ]; do
  if curl -sS http://localhost:8000/health >/dev/null 2>&1; then
    echo "Backend reachable"
    break
  fi
  COUNT=$((COUNT+1))
  sleep 1
done
if [ $COUNT -ge $MAX_WAIT ]; then
  echo "Backend did not become ready in time" >&2
  exit 2
fi

# call /plan
echo "Calling /plan"
resp=$(curl -sS -X POST http://localhost:8000/plan -H "Content-Type: application/json" -d '{"name":"ci-sample","domain":"web","goals":"","constraints":"","stack":"fullstack"}')
if [ -z "$resp" ]; then
  echo "Empty response from /plan" >&2
  exit 3
fi
echo "$resp"
exit 0
