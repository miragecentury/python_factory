#!/usr/bin/env bash

set -euo pipefail

pack build \
  python-poetry-empty \
  --buildpack paketo-buildpacks/python \
  --builder paketobuildpacks/builder-jammy-base
