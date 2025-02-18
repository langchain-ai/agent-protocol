# generated by fastapi-codegen:
#   filename:  openapi.json

from __future__ import annotations

from fastapi import FastAPI

from .routers import runs, stateless_runs, store, threads

app = FastAPI(
    title="Agent Protocol",
    version="0.1.3",
)

app.include_router(runs.router)
app.include_router(stateless_runs.router)
app.include_router(store.router)
app.include_router(threads.router)


@app.get("/")
async def root():
    return {"message": "Gateway of the App"}
