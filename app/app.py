import os
import socket

from flask import Flask, jsonify, render_template

app = Flask(__name__)

APP_ENV = os.getenv("APP_ENV", "DEV")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")


@app.route("/")
def home():
    return render_template(
        "index.html",
        environment=APP_ENV,
        version=APP_VERSION,
        hostname=socket.gethostname(),
    )


@app.route("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "environment": APP_ENV,
            "version": APP_VERSION,
            "hostname": socket.gethostname(),
        }
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)