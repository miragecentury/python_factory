FROM docker.io/library/python:3.12.4-slim-bullseye  as base
# hadolint shell=/bin/sh

# Prepare OS
ENV DEBIAN_FRONTEND=noninteractive \
    LC_ALL=C.UTF-8 \
    SHELL=/bin/bash

COPY docker/apt.conf /etc/apt/apt.conf.d/apt.conf

# Update OS
# hadolint ignore=DL3013
RUN \
    set -eux && \
    apt-get update && \
    apt-get upgrade -V && \
    pip install --no-cache-dir --upgrade pip && \
    # Clean (General)
    find /var/log -mtime -1 -type f -exec truncate -s 0 {} \; && \
    rm -rf \
        /var/lib/apt/lists/* \
        /var/cache/debconf/* \
        /var/log/*.gz \
        /var/log/*.log

ARG UID=1000
ARG GID=1000

# Prepare filesystem
RUN groupadd -g "${GID}" pythongroup && \
    useradd -l -u "${UID}" -g "${GID}" -d /opt/app -s /sbin/nologin pythonuser && \
    usermod -L pythonuser && \
    mkdir -p /opt/app/build && mkdir -p /opt/app/build/wheels && \
    chown -R pythonuser:pythongroup /opt/app

USER ${UID}

WORKDIR /opt/app

COPY --chown=pythonuser:pythongroup pyproject.toml /opt/app/pyproject.toml
COPY --chown=pythonuser:pythongroup build/wheels build/wheels

RUN pip install \
    --no-cache-dir \
    --progress-bar off \
    /opt/app/build/wheels/*.whl && \
    rm -rf /opt/app/build

ENTRYPOINT [ "python3", "-m", "python_poetry_empty" ]

CMD ["execute"]
