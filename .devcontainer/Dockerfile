FROM mcr.microsoft.com/devcontainers/python:3.13-bookworm

# Prevent install from crashing due to GPG key error
RUN rm -f /etc/apt/sources.list.d/yarn.list

RUN pip install --upgrade pip && \
    pip install --no-cache-dir "kelvin-sdk[mlflow]"