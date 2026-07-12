#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."

nginx -c "$(pwd)/deploy/local/nginx.local.conf" -s stop || true
supervisorctl -c deploy/local/supervisord.conf shutdown || true
