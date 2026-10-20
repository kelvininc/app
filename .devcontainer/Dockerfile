FROM mcr.microsoft.com/devcontainers/python:3.13-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Prevent install from crashing due to GPG key error
RUN rm -f /etc/apt/sources.list.d/yarn.list

RUN pip install --upgrade pip && \
    pip install --no-cache-dir "kelvin-sdk[mlflow]"
