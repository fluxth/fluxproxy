#!/usr/bin/env python3
from flask import Flask, request, abort, Response
from cryptography.fernet import Fernet
import json
import msgpack
import base64
import requests

VERSION = "1.0.0"

config = {}
with open("./config.json", "r") as f:
    config = json.load(f)

fernet = Fernet(config["secret"])

app = Flask(__name__)


@app.route("/")
def root():
    return f"fluxproxy/{VERSION}"


@app.route("/proxy")
def proxy():
    encrypted_req = request.args.get("req", "").strip()

    if len(encrypted_req) == 0:
        abort(400)

    serialized_req = fernet.decrypt(encrypted_req.encode("ascii"))
    req = msgpack.unpackb(serialized_req)

    url = req["url"]

    resp = requests.get(url)
    encrypted_resp = fernet.encrypt(resp.content)

    http_resp = Response(base64.urlsafe_b64decode(encrypted_resp))
    http_resp.headers["Content-Type"] = "application/octet-stream"
    return http_resp


if __name__ == "__main__":
    app.run("0.0.0.0", 7979)
