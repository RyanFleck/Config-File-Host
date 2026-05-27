# Config File Host

![Python 3.13](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=CCC)
[![Python Lint & Test](https://github.com/RyanFleck/Config-File-Host/actions/workflows/python-test.yml/badge.svg?branch=master)](https://github.com/RyanFleck/Config-File-Host/actions/workflows/python-test.yml)
[![Docker Image CI](https://github.com/RyanFleck/Config-File-Host/actions/workflows/docker-image.yml/badge.svg?branch=master)](https://github.com/RyanFleck/Config-File-Host/actions/workflows/docker-image.yml)

Flask app to host a single file from the filesystem with basic protections.

## Improvements

1. 100mb running size just to serve one file? Unreal. Fix.
1. Add Redis or a better backend for rate limiting.

## Test

```
uv run pytest
```

## Build

```
docker build -t config-file-host .
```

## Run

It is recommended to add a docker-compose file to deploy this app.

```bash
# docker-compose.yml
services:
  configfileservice:
    build:
      context: .
      dockerfile: Dockerfile

    container_name: secretfile

    ports:
      - "8809:8000"

    env_file:
      - .env

    # Optional: only needed if PROTECTED_FILE points to a host file
    volumes:
      - /your/folder/for/export:/data/export:ro

    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      # ...other Traefik config

    networks:
      - web

networks:
  web:
    external: true


# .env
DOWNLOAD_PATH=calendar
DOWNLOAD_KEY=strong
PROTECTED_FILE=/data/export/your-file.txt
```
