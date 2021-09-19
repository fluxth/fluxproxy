config.json: env
	./env/bin/python3 -c "from cryptography.fernet import Fernet; import json; print(json.dumps({'secret': Fernet.generate_key().decode('utf-8')}))" > config.json

env:
	virtualenv env
