# syntax=docker/dockerfile:1
# Base image for the nbops Cloud Agent environment.
# Stable system packages and the uv toolchain live here; project dependencies
# are installed later by the `install` phase against the checked-out source.
FROM python:3.12-slim-bookworm

# System packages required for git checkout, TLS, and building wheels.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*

# Install a pinned uv/uvx into a system-wide location that is on PATH for every user.
COPY --from=ghcr.io/astral-sh/uv:0.12.5 /uv /uvx /usr/local/bin/

# Container-friendly uv defaults: copy (don't hardlink) and precompile bytecode.
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

# Run as a non-root user matching the Cloud Agent checkout conventions.
RUN useradd --create-home --shell /bin/bash ubuntu
USER ubuntu
WORKDIR /home/ubuntu
