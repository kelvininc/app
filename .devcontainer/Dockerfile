FROM mcr.microsoft.com/devcontainers/python:3.13-bookworm

# To prevent GPG error 
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -

RUN pip install --upgrade pip && \
    pip install --no-cache-dir "kelvin-sdk[mlflow]"