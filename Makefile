.ONESHELL:

.DEFAULT_GOAL := run

venv/bin/activate: requirements.txt
	python -m venv venv
	chmod +x venv/bin/activate
	. ./venv/bin/activate
	$(PIP) install -r requirements.txt

venv: venv/bin/activate
	. ./venv/bin/activate

run: venv
	python producer.py

# clean:
# 	rm -rf __pycache__
# 	rm -rf v

.PHONY: run 