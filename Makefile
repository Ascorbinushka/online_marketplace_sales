SHELL := /bin/bash
PY = .venv/bin/python

.PHONY: up-services down-services up-af down-af gener-data

up-services:
	docker-compose -f docker-compose-services.yaml up -d --build

down-services:
	docker-compose -f docker-compose-services.yaml down


gener-data:
	python -m core.api.fetch_data