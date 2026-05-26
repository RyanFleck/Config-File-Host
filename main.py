from flask import Flask, abort, send_file, request
import os
import sys
import secrets
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()  # reads variables from a .env file and sets them in os.environ

log = logging.getLogger(__name__)
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
limiter = Limiter(
    key_func=get_remote_address, app=app, default_limits=["10 per minute"]
)
# TODO: Add a proper backend for the rate limiter :)

# Pull from environment variables:
SECRET_PATH = os.environ.get("DOWNLOAD_PATH")
SECRET_KEY = os.environ.get("DOWNLOAD_KEY")
FILE_PATH = os.environ.get("PROTECTED_FILE")

if not SECRET_KEY:
    raise RuntimeError("Set DOWNLOAD_KEY env var")

if not SECRET_PATH:
    raise RuntimeError("Set DOWNLOAD_PATH env var")

if not FILE_PATH:
    raise RuntimeError("Set PROTECTED_FILE env var")

# Expand file path:
FILE_PATH = os.path.expanduser(FILE_PATH)
FILE_PATH = os.path.abspath(FILE_PATH)

# Initial check for missing file
if not os.path.exists(FILE_PATH):
    raise RuntimeError(f"Missing file: {FILE_PATH}")


@app.route("/")
@limiter.limit("10 per minute")
def home():
    """Simple 200 response for homepage."""
    return "OK"


@app.route("/download/<secret_path>")
@limiter.limit("10 per minute")
def download(secret_path):
    """Provides the protected file if path and key are correct."""
    log.info("Incoming request from IP %s", request.remote_addr)

    # 404 if path doesn't exist
    # Constant-time comparison prevents timing attacks
    if not secrets.compare_digest(secret_path, SECRET_PATH):
        log.info("Bad path: %s", secret_path)
        abort(404)

    # 404 if file doesn't exist as-configured
    if not os.path.exists(FILE_PATH):
        log.info("Can't find file on filesystem: %s", FILE_PATH)
        abort(404)

    # Fetch key from url parameters
    key = request.args.get("key")

    # 404 if blank or missing key
    if not key:
        log.info("Request is missing key.")
        abort(404)

    # 404 if bad key
    if not secrets.compare_digest(key, SECRET_KEY):
        log.info("Request has bad key.")
        abort(404)

    log.info("Returning file to IP %s", request.remote_addr)
    return send_file(
        FILE_PATH,
        as_attachment=True,
        download_name=os.path.basename(FILE_PATH),
        conditional=True,
    )


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    logging.getLogger("werkzeug").setLevel(logging.INFO)

    log.info("Started program.")
    app.run(host="0.0.0.0", port=5000)
