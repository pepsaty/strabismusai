#!/usr/bin/env bash
set -Eeuo pipefail

SRC="/storage/emulated/0/neumorphism-ui-bootstrap-1.0.0/neumorphism-ui-bootstrap-1.0.0/share"
REPO="$HOME/strabismusai"

cp "$SRC/StrabismusAI-Pro.single.html" "$REPO/index.html"
cp "$SRC/strabismus.single.html"       "$REPO/textbook.html"
: > "$REPO/.nojekyll"

cd "$REPO"
git add -A
git commit -m "Update single-file build"
git push
