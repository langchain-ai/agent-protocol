gen-server:
	poetry run fastapi-codegen --input ../openapi.json --output-model-type pydantic_v2.BaseModel --output ../server/ap_server --generate-routers --disable-timestamp
	poetry run autoflake -i -r --remove-all-unused-imports --expand-star-imports --ignore-pass-statements ../server/ap_server
	rm ../server/ap_server/dependencies.py
	sed -i '' 's|from \.\.dependencies|from ..models|g' ../server/ap_server/routers/*.py
	sed -i '' 's|Action1|Action|g' ../server/ap_server/routers/*.py
	sed -i '' 's|from fastapi import APIRouter|from typing import Annotated\n\nfrom fastapi import APIRouter, Query|g' ../server/ap_server/routers/store.py
	sed -i '' 's|namespace: Optional\[Namespace\] = None|namespace: Annotated\[list\[str\] \| None, Query\(\)\] = None|g' ../server/ap_server/routers/store.py
	poetry run ruff format ../server/ap_server
	touch ../server/ap_server/__init__.py
	touch ../server/ap_server/routers/__init__.py
