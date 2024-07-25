#!/usr/bin/env bash

# Poetry setup
poetry env use python3.12
poetry install --with test
poetry update --sync

# Pre-commit setup
pre-commit install

cat > .env <<EOF
PATH="./src:./tests:\$PATH"
PYTHONPATH="./src:./tests:\$PYTHONPATH"

EOF

mkdir -p build/wheels
