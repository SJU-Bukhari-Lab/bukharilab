#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! python3 -c 'import PIL' >/dev/null 2>&1; then
  echo "Installing Pillow for local deploy-output optimization..."
  python3 -m pip install --user Pillow==11.3.0
fi

rm -rf _site .jekyll-cache
bundle exec jekyll build
python3 scripts/optimize_built_site.py --site-dir _site

echo
echo "Optimized site built at: $ROOT/_site"
echo "Preview with: python3 -m http.server 4000 -d _site"
