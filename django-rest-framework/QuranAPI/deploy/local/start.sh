#!/usr/bin/env bash
# Starts the local "server" stack: supervisor -> gunicorn (unix socket) -> nginx (:8088)
set -euo pipefail
cd "$(dirname "$0")/../.."

mkdir -p /tmp/quranapi-run deploy/local/logs

supervisord -c deploy/local/supervisord.conf
sleep 1
supervisorctl -c deploy/local/supervisord.conf status

nginx -c "$(pwd)/deploy/local/nginx.local.conf"

echo "Swagger UI:  http://127.0.0.1:8088/api/"
echo "Surah list:  http://127.0.0.1:8088/api/v1/surah/"
