.PHONY: gen-server gen-client-python format-tooling format-client-python format-server format-openapi format lint-tooling lint-client-python lint-server lint-openapi lint

gen-server:
	uv run fastapi-codegen --input ../openapi.json --output-model-type pydantic_v2.BaseModel --output ../server/ap_server --generate-routers --disable-timestamp
	uv run autoflake -i -r --remove-all-unused-imports --expand-star-imports --ignore-pass-statements ../server/ap_server
	rm ../server/ap_server/dependencies.py
	sed -i '' 's|from \.\.dependencies|from ..models|g' ../server/ap_server/routers/*.py
	sed -i '' 's|Action1|Action|g' ../server/ap_server/routers/*.py
	sed -i '' 's|from fastapi import APIRouter|from typing import Annotated\n\nfrom fastapi import APIRouter, Query|g' ../server/ap_server/routers/store.py
	sed -i '' 's|namespace: Optional\[Namespace\] = None|namespace: Annotated\[list\[str\] \| None, Query\(\)\] = None|g' ../server/ap_server/routers/store.py
	sed -i '' 's|response_model=None,|response_model=None, status_code=204,|g' ../server/ap_server/routers/*.py
	uv run ruff format ../server/ap_server
	touch ../server/ap_server/__init__.py
	touch ../server/ap_server/routers/__init__.py

gen-client-python:
	docker run --rm -v "${PWD}/..:/local" openapitools/openapi-generator-cli:v7.13.0 generate \
    -i /local/openapi.json \
    -g python \
    -o /local/client-python \
    --package-name=ap_client
	sed -i '' 's|elif klass == object|elif klass is object|g' ../client-python/ap_client/*.py
	uv run ruff format ../client-python/ap_client
	uv run ruff check --fix --unsafe-fixes ../client-python/ap_client

format-tooling:
	uv run ruff format .
	uv run ruff check --fix --unsafe-fixes .

format-client-python:
	uv run ruff format ../client-python/ap_client
	uv run ruff check --fix --unsafe-fixes ../client-python/ap_client

format-server:
	uv run ruff format ../server/ap_server
	uv run ruff check --fix --unsafe-fixes ../server/ap_server

format-openapi:
	npx --yes prettier@$(PRETTIER_VERSION) --write "../openapi.json"

format: format-tooling format-client-python format-server format-openapi

lint-tooling:
	uv run ruff check .

lint-client-python:
	uv run ruff check ../client-python/ap_client

lint-server:
	uv run ruff check ../server/ap_server

lint: lint-tooling lint-client-python lint-server

