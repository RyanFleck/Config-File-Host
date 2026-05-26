# Config-File-Host

Flask app to host a single file from the filesystem with protection.

## Build

```
docker build -t config-file-host .
```

## Run

```bash
# docker-compose.yml
services:
  flask-app:
    container_name: protected-download-app
    restart: unless-stopped
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    env_file:
      - .env
    # Optional: only needed if PROTECTED_FILE points to a host file
    volumes:
      - /your/folder/for/export:/data/export:ro
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:8000/"]
      interval: 30s
      timeout: 5s
      retries: 3

# .env
DOWNLOAD_PATH=calendar
DOWNLOAD_KEY=strong
PROTECTED_FILE=/data/export/your-file.txt
```
