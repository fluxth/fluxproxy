#!/usr/bin/env python3
import sys
import json
import msgpack
from cryptography.fernet import Fernet


def main():
    config = {}
    with open("config.json", "r") as f:
        config = json.load(f)

    if len(sys.argv) <= 1:
        print("Error: No data provided", file=sys.stderr)
        exit(1)

    fernet = Fernet(config["secret"])

    payload = {}
    for arg in sys.argv[1:]:
        if "=" not in arg:
            print(f"Warning: No '=' detected in '{arg}', ignoring.", file=sys.stderr)
            continue

        parts = arg.split("=")
        key = parts[0]
        value = "=".join(parts[1:])

        payload[key] = value

    serialized_payload = msgpack.packb(payload)
    print(fernet.encrypt(serialized_payload).decode("utf-8"))


if __name__ == "__main__":
    main()
