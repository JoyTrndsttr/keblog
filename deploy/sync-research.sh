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

workbench_source="$repository/workbench"
stamp="$cache/workbench.sha256"
checksum=$(python3 - "$workbench_source" <<'PYCHECKSUM'
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
hasher = hashlib.sha256()
for path in sorted(item for item in root.rglob("*") if item.is_file()):
    relative = path.relative_to(root).as_posix().encode()
    hasher.update(relative)
    hasher.update(b"\0")
    hasher.update(hashlib.sha256(path.read_bytes()).digest())
    hasher.update(b"\0")
print(hasher.hexdigest())
PYCHECKSUM
)
if [[ ! -f "$stamp" || ! -d "$cache/workbench" || "$(cat "$stamp")" != "$checksum" ]]; then
  staging=$(mktemp -d "$cache/.workbench-next.XXXXXX")
  previous="$cache/.workbench-previous"
  trap 'rm -rf "$staging"' EXIT
  mkdir -p "$staging/workbench"
  cp -a "$workbench_source/." "$staging/workbench/"
  python3 - "$workbench_source" "$staging" <<'PYEXTRACT'
import sys
import tarfile
from pathlib import Path
from pathlib import PurePosixPath

source, destination = map(Path, sys.argv[1:])
archives = sorted(source.rglob("*-latest.tar.gz"))
if not archives:
    raise SystemExit("no workbench archives found")

total_archive_bytes = 0
total_uncompressed_bytes = 0
for archive in archives:
    total_archive_bytes += archive.stat().st_size
    if archive.stat().st_size > 95_000_000:
        raise SystemExit(f"workbench archive is too large: {archive}")
    with tarfile.open(archive, "r:gz") as bundle:
        members = bundle.getmembers()
        uncompressed_bytes = sum(item.size for item in members)
        if len(members) > 5000 or uncompressed_bytes > 256_000_000:
            raise SystemExit(f"workbench archive exceeds publication limits: {archive}")
        total_uncompressed_bytes += uncompressed_bytes
        for item in members:
            path = PurePosixPath(item.name)
            if path.is_absolute() or not path.parts or path.parts[0] != "workbench" or ".." in path.parts:
                raise SystemExit(f"unsafe workbench path: {item.name}")
            if path.as_posix() in {"workbench/index.html", "workbench/catalog.json", "workbench/manifest.json", "workbench/README.md"}:
                raise SystemExit(f"archive may not replace workbench index metadata: {item.name}")
            if not (item.isdir() or item.isfile()):
                raise SystemExit(f"unsupported workbench entry: {item.name}")
        bundle.extractall(destination, members=members, filter="data")
if total_archive_bytes > 100_000_000 or total_uncompressed_bytes > 1_000_000_000:
    raise SystemExit("combined workbench archives exceed publication limits")
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
