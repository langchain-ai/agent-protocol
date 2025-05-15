"""
# List tools
curl -X POST http://localhost:8000/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json,text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'

# Call tools
curl -X POST "http://localhost:8000/mcp/" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json,text/event-stream" \
     -d '{
       "jsonrpc": "2.0",
       "id": 1,
       "method": "tools/call",
       "params": {
         "name": "agent_1",
         "arguments": {
           "foo": "bar",
           "count": 3
         }
       }
     }'
"""

import json
from typing import Any, Sequence

import ap_client
from mcp import Tool as MCPTool
from mcp.server.fastmcp import FastMCP
from mcp.server.lowlevel import Server
from mcp.types import TextContent

URL = "http://localhost:8002"

server = Server(name="Agent Protocol MCP")
configuration = ap_client.Configuration(host=URL)


class AgentProtocolMCP(FastMCP):
    """Agent Protocol MCP."""

    @server.list_tools()
    async def list_tools(self) -> list[MCPTool]:
        """Override list tools to allow setting it dynamically"""
        with ap_client.ApiClient(configuration) as api_client:
            # Create an instance of the API class
            api_instance = ap_client.AgentsApi(api_client)
            response = api_instance.search_agents_with_http_info(
                ap_client.models.SearchAgentsRequest()
            )

            mcp_tools = []
            for agent in response.data:
                # Can parallelize this
                schema_response = api_instance.get_agent_schemas(
                    agent_id=agent.agent_id
                )
                mcp_tools.append(
                    MCPTool(
                        # Choosing the agent ID as the convention for the name.
                        # This is because MCP has no mechanism to avoid name collisions
                        # so the name should be unique.
                        name=agent.id,
                        # You could prepend the actual agent name to the description.
                        description=agent.description,
                        inputSchema=schema_response.input_schema,
                    )
                )
        return mcp_tools

    @server.call_tool()
    async def call_tool(
        self,
        name: str,
        arguments: dict[str, Any],
    ) -> Sequence["TextContent | ImageContent | EmbeddedResource"]:
        """List tool."""
        with ap_client.ApiClient(configuration) as api_client:
            # Create an instance of the API class
            runs_api = ap_client.RunsApi(api_client)
            response = runs_api.create_and_wait_run(
                ap_client.RunCreate(
                    # Not using a state since this is a stateless server
                    thread_id=None,
                    agent_id=name,
                    input=arguments,
                )
            )
            # The easiest thing is to encode the values as JSON and put them
            # into a TextContent object.
            # You can use other return types if they are appropriate for your use
            # case.
            return [TextContent(type="text", text=json.dumps(response.values))]


mcp = AgentProtocolMCP(
    "StatelessServer",
    # Our server implementation is stateless, but you could use a stateful
    # implementation if it makes sense for your use case.
    stateless_http=True,
    # Currently JSON response makes more sense since we're only doing tool calls
    # and aren't sending progress notifications.
    json_response=True,
)
app = mcp.streamable_http_app()
