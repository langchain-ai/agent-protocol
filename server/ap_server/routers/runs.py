# generated by fastapi-codegen:
#   filename:  openapi.json

from __future__ import annotations

from fastapi import APIRouter

from ..models import (
    Action,
    Any,
    ErrorResponse,
    Optional,
    Run,
    RunCreateStateful,
    ThreadsThreadIdRunsGetResponse,
    UUID,
    Union,
)

router = APIRouter(tags=["Runs"])


@router.get(
    "/threads/{thread_id}/runs",
    response_model=ThreadsThreadIdRunsGetResponse,
    responses={"404": {"model": ErrorResponse}, "422": {"model": ErrorResponse}},
    tags=["Runs"],
)
def list_runs_http_threads__thread_id__runs_get(
    thread_id: UUID, limit: Optional[int] = 10, offset: Optional[int] = 0
) -> Union[ThreadsThreadIdRunsGetResponse, ErrorResponse]:
    """
    List Runs
    """
    pass


@router.post(
    "/threads/{thread_id}/runs",
    response_model=Run,
    responses={
        "404": {"model": ErrorResponse},
        "409": {"model": ErrorResponse},
        "422": {"model": ErrorResponse},
    },
    tags=["Runs"],
)
def create_run_threads__thread_id__runs_post(
    thread_id: UUID, body: RunCreateStateful = ...
) -> Union[Run, ErrorResponse]:
    """
    Create Background Run
    """
    pass


@router.post(
    "/threads/{thread_id}/runs/stream",
    response_model=Any,
    responses={
        "404": {"model": ErrorResponse},
        "409": {"model": ErrorResponse},
        "422": {"model": ErrorResponse},
    },
    tags=["Runs"],
)
def stream_run_threads__thread_id__runs_stream_post(
    thread_id: UUID, body: RunCreateStateful = ...
) -> Union[Any, ErrorResponse]:
    """
    Create Run, Stream Output
    """
    pass


@router.post(
    "/threads/{thread_id}/runs/wait",
    response_model=Any,
    responses={
        "404": {"model": ErrorResponse},
        "409": {"model": ErrorResponse},
        "422": {"model": ErrorResponse},
    },
    tags=["Runs"],
)
def wait_run_threads__thread_id__runs_wait_post(
    thread_id: UUID, body: RunCreateStateful = ...
) -> Union[Any, ErrorResponse]:
    """
    Create Run, Wait for Output
    """
    pass


@router.get(
    "/threads/{thread_id}/runs/{run_id}",
    response_model=Run,
    responses={"404": {"model": ErrorResponse}, "422": {"model": ErrorResponse}},
    tags=["Runs"],
)
def get_run_http_threads__thread_id__runs__run_id__get(
    thread_id: UUID, run_id: UUID = ...
) -> Union[Run, ErrorResponse]:
    """
    Get Run
    """
    pass


@router.delete(
    "/threads/{thread_id}/runs/{run_id}",
    response_model=None,
    status_code=204,
    responses={"404": {"model": ErrorResponse}, "422": {"model": ErrorResponse}},
    tags=["Runs"],
)
def delete_run_threads__thread_id__runs__run_id__delete(
    thread_id: UUID, run_id: UUID = ...
) -> Optional[ErrorResponse]:
    """
    Delete Run
    """
    pass


@router.post(
    "/threads/{thread_id}/runs/{run_id}/cancel",
    response_model=None,
    status_code=204,
    responses={"404": {"model": ErrorResponse}, "422": {"model": ErrorResponse}},
    tags=["Runs"],
)
def cancel_run_http_threads__thread_id__runs__run_id__cancel_post(
    thread_id: UUID,
    run_id: UUID = ...,
    wait: Optional[bool] = False,
    action: Optional[Action] = "interrupt",
) -> Optional[ErrorResponse]:
    """
    Cancel Run
    """
    pass


@router.get(
    "/threads/{thread_id}/runs/{run_id}/stream",
    response_model=Any,
    responses={"404": {"model": ErrorResponse}, "422": {"model": ErrorResponse}},
    tags=["Runs"],
)
def stream_run_http_threads__thread_id__runs__run_id__join_get(
    thread_id: UUID, run_id: UUID = ...
) -> Union[Any, ErrorResponse]:
    """
    Stream output from Run
    """
    pass


@router.get(
    "/threads/{thread_id}/runs/{run_id}/wait",
    response_model=Any,
    responses={"404": {"model": ErrorResponse}, "422": {"model": ErrorResponse}},
    tags=["Runs"],
)
def join_run_http_threads__thread_id__runs__run_id__join_get(
    thread_id: UUID, run_id: UUID = ...
) -> Union[Any, ErrorResponse]:
    """
    Wait for Run output
    """
    pass
