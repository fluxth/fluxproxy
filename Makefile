.PHONY: run

config.json: env
	@./env/bin/python3 -c "from cryptography.fernet import Fernet; import json; print(json.dumps({'secret': Fernet.generate_key().decode('utf-8')}))" > config.json
	$(info config.json generated)

run: config.json
	@uwsgi --http 0.0.0.0:7979 --module fluxproxy:app

env:
	virtualenv env
	$(info virtualenv created)
