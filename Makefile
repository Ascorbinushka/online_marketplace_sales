SHELL := /bin/bash
PY = .venv/bin/python

.PHONY: up-services down-services up-af down-af gener-data

up-services:
	docker-compose -f docker-compose-services.yaml up -d --build

down-services:
	docker-compose -f docker-compose-services.yaml down
up-af:
	docker-compose -f docker-compose-af.yaml up -d --build

down-af:
	docker-compose -f docker-compose-af.yaml down

gener-data:
	python -m airflow.dags.core.api.fetch_data


up-mb:
	docker-compose -f docker-compose-metabase.yml up -d --build

down-mb:
	docker-compose -f docker-compose-metabase.yml down