#!/usr/bin/env bash
set -euo pipefail

repository=/var/lib/wangke-site/research-source
remote=git@github-causal-review:JoyTrndsttr/causal-review.git
cache=/var/lib/wangke-site/research-cache

if [[ ! -d "$repository/.git" ]]; then
  git clone --filter=blob:none --no-checkout "$remote" "$repository"
  git -C "$repository" sparse-checkout init --cone
  git -C "$repository" sparse-checkout set documents workbench
  git -C "$repository" checkout master
else
  [[ -z "$(git -C "$repository" status --porcelain)" ]]
  git -C "$repository" sparse-checkout set documents workbench
  git -C "$repository" pull --ff-only
fi

find "$repository/documents" -type d -exec chmod 755 {} +
find "$repository/documents" -type f -exec chmod 644 {} +
mkdir -p "$cache"
install -m 644 "$repository/documents/研究记录.md" "$cache/research-record.md.next"
mv "$cache/research-record.md.next" "$cache/research-record.md"

archive="$repository/workbench/workbench-latest.tar.gz"
stamp="$cache/workbench.sha256"
checksum=$(sha256sum "$archive" | awk '{print $1}')
if [[ ! -f "$stamp" || ! -d "$cache/workbench" || "$(cat "$stamp")" != "$checksum" ]]; then
  staging=$(mktemp -d "$cache/.workbench-next.XXXXXX")
  previous="$cache/.workbench-previous"
  trap 'rm -rf "$staging"' EXIT
  python3 - "$archive" "$staging" <<'PYEXTRACT'
import sys
import tarfile
from pathlib import PurePosixPath

archive, destination = sys.argv[1:]
with tarfile.open(archive, "r:gz") as bundle:
    members = bundle.getmembers()
    if len(members) > 5000 or sum(item.size for item in members) > 100 * 1024 * 1024:
        raise SystemExit("workbench archive exceeds publication limits")
    for item in members:
        path = PurePosixPath(item.name)
        if path.is_absolute() or not path.parts or path.parts[0] != "workbench" or ".." in path.parts:
            raise SystemExit(f"unsafe workbench path: {item.name}")
        if not (item.isdir() or item.isfile()):
            raise SystemExit(f"unsupported workbench entry: {item.name}")
    bundle.extractall(destination, members=members, filter="data")
PYEXTRACT
  [[ -f "$staging/workbench/index.html" ]]
  find "$staging/workbench" -type d -exec chmod 755 {} +
  find "$staging/workbench" -type f -exec chmod 644 {} +
  rm -rf "$previous"
  if [[ -d "$cache/workbench" ]]; then mv "$cache/workbench" "$previous"; fi
  mv "$staging/workbench" "$cache/workbench"
  printf '%s\n' "$checksum" > "$stamp.next"
  mv "$stamp.next" "$stamp"
  rm -rf "$previous" "$staging"
  trap - EXIT
fi
