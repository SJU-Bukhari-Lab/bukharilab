#!/usr/bin/env bash
set -euo pipefail

repo="${1:-.}"
cd "$repo"

rm -rf _site .jekyll-cache
bundle exec jekyll build
python3 scripts/public_release_audit.py .
python3 scripts/audit_faculty_feedback.py .
python3 scripts/refresh_project_images.py . --check
bundle exec htmlproofer ./_site --disable-external --allow-hash-href
python3 scripts/audit_content_integrity.py .
python3 scripts/audit_external_links.py ./_site
git diff --check

echo "Website validation passed."
