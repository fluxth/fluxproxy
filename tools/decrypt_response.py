#!/usr/bin/env python3

import sys
import json
import base64
from cryptography.fernet import Fernet


def main():
    config = {}
    with open("config.json", "r") as f:
        config = json.load(f)

    fernet = Fernet(config["secret"])

    payload = sys.stdin.buffer.read()
    b64_payload = base64.urlsafe_b64encode(payload)

    print(fernet.decrypt(b64_payload).decode("utf-8"))


if __name__ == "__main__":
    main()
