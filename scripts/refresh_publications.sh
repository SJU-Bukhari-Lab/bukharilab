#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${TMPDIR:-/tmp}/bukharilab-citations-venv"

cd "$ROOT"

if [[ ! -f "$VENV/bin/activate" ]]; then
  rm -rf "$VENV"
  python3 -m venv "$VENV"
fi

# shellcheck disable=SC1091
source "$VENV/bin/activate"

python -m pip install --disable-pip-version-check --quiet \
  -r _cite/requirements.txt \
  certifi

export SSL_CERT_FILE="$(python -c 'import certifi; print(certifi.where())')"
export REQUESTS_CA_BUNDLE="$SSL_CERT_FILE"

python _cite/cite.py

echo
echo "Publication record refreshed at _data/citations.yaml"
