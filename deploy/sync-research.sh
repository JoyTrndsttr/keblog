#!/usr/bin/env bash
set -euo pipefail

repository=/var/lib/wangke-site/research-source
remote=git@github-causal-review:JoyTrndsttr/causal-review.git

if [[ ! -d "$repository/.git" ]]; then
  git clone --filter=blob:none --no-checkout "$remote" "$repository"
  git -C "$repository" sparse-checkout init --cone
  git -C "$repository" sparse-checkout set documents
  git -C "$repository" checkout master
else
  [[ -z "$(git -C "$repository" status --porcelain)" ]]
  git -C "$repository" pull --ff-only
fi

find "$repository/documents" -type d -exec chmod 755 {} +
find "$repository/documents" -type f -exec chmod 644 {} +

cache=/var/lib/wangke-site/research-cache
mkdir -p "$cache"
install -m 644 "$repository/documents/研究记录.md" "$cache/research-record.md.next"
mv "$cache/research-record.md.next" "$cache/research-record.md"
