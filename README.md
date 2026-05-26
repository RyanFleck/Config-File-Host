# Config-File-Host

Flask app to host a single file from the filesystem with protection.

**ToDo**:

1. 100mb running size just to serve one file? Unreal. Fix.

## Build

```
docker build -t config-file-host .
```

## Run

```bash
# docker-compose.yml
services:
  secretfile:
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
