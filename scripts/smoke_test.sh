#!/usr/bin/env bash
# Usage: SERVICE_URL=https://tardis-xxx.run.app bash smoke_test.sh
set -euo pipefail
URL="${SERVICE_URL:-http://localhost:8080}"
TOKEN="${AUTH_TOKEN:-}"
AUTH=""
[ -n "$TOKEN" ] && AUTH="-H \"Authorization: Bearer $TOKEN\""

echo "==> Testing /health"
curl -sf $AUTH "$URL/health" | python3 -m json.tool

echo ""
echo "==> Testing /act (approval gate — should return skipped)"
curl -sf $AUTH -X POST "$URL/act" \
  -H "Content-Type: application/json" \
  -d '{"type":"draft_email","owner":"liz","reason":"test","approval_required":true,"payload":{"to":"test@example.com","subject":"Test","body":"Hello"}}' \
  | python3 -m json.tool

echo ""
echo "All smoke tests passed."
