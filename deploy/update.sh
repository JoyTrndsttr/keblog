#!/usr/bin/env bash
# Run as root on lab-vps after reviewing and pushing the desired commit.
set -euo pipefail
cd /opt/keblog
if [[ -n "$(git status --porcelain)" ]]; then
  echo "Checkout has local changes; review and commit/push them before updating." >&2
  exit 1
fi
previous=$(git rev-parse HEAD)
git pull --ff-only
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 scripts/build.py
install -m 644 deploy/keblog.service /etc/systemd/system/keblog.service
systemctl daemon-reload
systemctl restart keblog
for attempt in {1..10}; do
  if curl --noproxy '*' -fsS http://127.0.0.1:8080/api/v1/bootstrap >/dev/null; then
    echo "Deployed $(git rev-parse --short HEAD); previous revision: $previous"
    exit 0
  fi
  sleep 1
done
echo "Health check failed. Previous revision: $previous; inspect journalctl -u keblog." >&2
exit 1
