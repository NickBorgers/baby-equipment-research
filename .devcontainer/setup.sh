#!/usr/bin/env bash
# Clone -> open in devcontainer -> `make check` works. Nothing else required.
set -euo pipefail

pip install --user --quiet --disable-pip-version-check -r requirements.txt

# jq is what carries the host's Claude Code identity into the container: the
# util bootstrap skips system packages inside a container (UTIL_SKIP_PACKAGES),
# so seed_claude_identity finds no jq, says so, and leaves you to log in again.
# Installing it here — before dcs/dcr runs that bootstrap — avoids the prompt.
if ! command -v jq >/dev/null 2>&1; then
  sudo apt-get update -qq && sudo apt-get install -y -qq jq
fi

echo
echo "baby-equipment is ready."
echo "  make check   # validate the candidate data, confirm docs are current, run tests"
echo "  make docs    # regenerate docs/ after editing any YAML"
echo "  make fit     # print the compatibility + fit report"
echo "  make serve   # preview the GitHub Pages site at localhost:8000"
echo
