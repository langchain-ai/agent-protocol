# generated by fastapi-codegen:
#   filename:  openapi.json

from __future__ import annotations

from fastapi import APIRouter

from ..models import (
    Agent,
    AgentSchemas,
    AgentsSearchPostRequest,
    AgentsSearchPostResponse,
    ErrorResponse,
    Union,
)

router = APIRouter(tags=["Agents"])


@router.post(
    "/agents/search",
    response_model=AgentsSearchPostResponse,
    responses={"404": {"model": ErrorResponse}, "422": {"model": ErrorResponse}},
    tags=["Agents"],
)
def search_agents(
    body: AgentsSearchPostRequest,
) -> Union[AgentsSearchPostResponse, ErrorResponse]:
    """
    Search Agents
    """
    pass


@router.get(
    "/agents/{agent_id}",
    response_model=Agent,
    responses={"404": {"model": ErrorResponse}},
    tags=["Agents"],
)
def get_agent(agent_id: str) -> Union[Agent, ErrorResponse]:
    """
    Get Agent
    """
    pass


@router.get(
    "/agents/{agent_id}/schemas",
    response_model=AgentSchemas,
    responses={"404": {"model": ErrorResponse}, "422": {"model": ErrorResponse}},
    tags=["Agents"],
)
def get_agent_schemas(agent_id: str) -> Union[AgentSchemas, ErrorResponse]:
    """
    Get Agent Schemas
    """
    pass
