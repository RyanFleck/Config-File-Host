# Config-File-Host

Flask app to host a single file from the filesystem with protection.

## Build

```
docker build -t config-file-host .
```

## Run

```
docker run -d \
  --name config-file-host \
  -p 8000:8000 \
  -e DOWNLOAD_PATH='the-file' \
  -e DOWNLOAD_SECRET='your-long-random-secret' \
  -e PROTECTED_FILE='/files/myfile.zip' \
  -v ~/Documents:/files:ro \
  config-file-host
```
