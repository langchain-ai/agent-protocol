# Agent Protocol

Agent Protocol is our attempt at codifying the framework-agnostic APIs that are needed to serve LLM agents in production. This document explains the purpose of the protocol and makes the case for each of the endpoints in the spec. We finish by listing some roadmap items for the future.

See the [full OpenAPI docs](https://langchain-ai.github.io/agent-protocol/api.html) and the [JSON spec](https://langchain-ai.github.io/agent-protocol/openapi.json).

[LangGraph Platform](https://www.langchain.com/pricing-langgraph-platform) implements a superset of this protocol, but we very much welcome other implementations from the community.

## Resources

- [Agent Protocol OpenAPI Docs](https://langchain-ai.github.io/agent-protocol/api.html)
- [Agent Protocol JSON Spec](https://langchain-ai.github.io/agent-protocol/openapi.json)
- [Agent Streaming Protocol](./streaming/) - streaming primitives, CDDL schema, and generated Python/TypeScript bindings for live agent execution
- [Agent Protocol Python Server Stubs](./server/) - a Python server, using Pydantic V2 and FastAPI, auto-generated from the OpenAPI spec
- [LangGraph.js API](https://github.com/langchain-ai/langgraphjs-api/tree/main/libs/langgraph-api) - an open-source implementation of this protocol, for LangGraph.js agents, using in-memory storage
- [LangGraph Platform](https://www.langchain.com/pricing-langgraph-platform) - a commercial platform that implements a superset of this protocol for deploying any LLM agent in production
- [Self-hosted async subagent server (Python)](https://github.com/langchain-ai/deepagents/tree/main/examples/async-subagent-server) - a Python example of a self-hosted agent implementing this protocol, designed to be invoked as an async subagent
- [Self-hosted async subagent server (TypeScript)](https://github.com/langchain-ai/deepagentsjs/tree/main/examples/async-subagent-server) - a TypeScript example of a self-hosted agent implementing this protocol, designed to be invoked as an async subagent

## Why Agent Protocol

What is the right API to serve an LLM application in production? We believe it’s centered around 3 important concepts:

- Runs: APIs for executing an agent
- Threads: APIs to organize multi-turn executions of agents
- Store: APIs to work with long-term memory

Let’s dive deeper into each one, starting with the requirements, and then presenting the Protocol endpoints that meet these requirements.

## Stateless Runs: one-shot interactions

In some cases, you may want to create a thread and run in one request, and have the thread be deleted after the run concludes. This is useful for ephemeral or stateless interactions, where you don’t need to keep track of the thread’s state.

- [`POST /runs/wait`](https://langchain-ai.github.io/agent-protocol/api.html#tag/runs/POST/runs/wait) - Create an ephemeral run, and wait for its final output, which is returned in the response.
- [`POST /runs/stream`](https://langchain-ai.github.io/agent-protocol/api.html#tag/runs/POST/runs/stream) - Create an ephemeral run, and stream output as produced.

## Threads: multi-turn interactions

What APIs do you need to enable multi-turn interactions?

- Persistent state
  - Get and update state
  - Track history of past states of a thread, modelled as an append-only log of states
  - Optimize storage by storing only diffs between states
- Concurrency controls
  - Ensure that only one run per thread is active at a time
  - Customizable handling of concurrent runs (interrupt, enqueue, interrupt or rollback)
- CRUD endpoints for threads
  - List threads by user, or other metadata
  - List threads by status (idle, interrupted, errored, finished)
  - Copy or delete threads

Endpoints:

- [`POST /threads`](https://langchain-ai.github.io/agent-protocol/api.html#tag/threads/POST/threads) - Create a thread.
- [`POST /threads/search`](https://langchain-ai.github.io/agent-protocol/api.html#tag/threads/POST/threads/search) - Search threads.
- [`GET /threads/{thread_id}`](https://langchain-ai.github.io/agent-protocol/api.html#tag/threads/GET/threads/%7Bthread_id%7D) - Get a thread.
- [`GET /threads/{thread_id}/history`](https://langchain-ai.github.io/agent-protocol/api.html#tag/threads/GET/threads/%7Bthread_id%7D/history) - Browse past revisions of a thread’s state. Revisions are created by runs, or through the PATCH endpoint below.
- [`POST /threads/{thread_id}/copy`](https://langchain-ai.github.io/agent-protocol/api.html#tag/threads/POST/threads/%7Bthread_id%7D/copy) - Create an independent copy of a thread.
- [`DELETE /threads/{thread_id}`](https://langchain-ai.github.io/agent-protocol/api.html#tag/threads/DELETE/threads/%7Bthread_id%7D) - Delete a thread.
- [`PATCH /threads/{thread_id}`](https://langchain-ai.github.io/agent-protocol/api.html#tag/threads/PATCH/threads/%7Bthread_id%7D) - Update a thread's values or metadata. Updating values creates a new revision in the thread's history.

## Agents: Introspection

Before you make use of an agent, it's sometimes useful to know what it can do, what inputs it accepts, what it returns, etc. This is where the introspection endpoints come in.

Endpoints:

- [`POST /agents/search`](https://langchain-ai.github.io/agent-protocol/api.html#tag/agents/POST/agents/search) - List all agents, optionally filtered by metadata or name.
- [`GET /agents/{agent_id}`](https://langchain-ai.github.io/agent-protocol/api.html#tag/agents/GET/agents/%7Bagent_id%7D) - Get basic information about an agent, including its name, description, metadata.
- [`GET /agents/{agent_id}/schemas`](https://langchain-ai.github.io/agent-protocol/api.html#tag/agents/GET/agents/%7Bagent_id%7D/schemas) - Get the input, output, state and config schemas for an agent. All schemas are represented in JSON Schema format.

## Background Runs: Atomic agent executions

What do we need out of an API to execute an agent?

- Support the two paradigms for launching a run
  - Fire and forget, ie. launch a run in the background, but don’t wait for it to finish
  - Waiting on a reply (blocking or polling), ie. launch a run and wait/stream its output
- Support CRUD for agent executions
  - List and get runs
  - Cancel and delete runs
- Flexible ways to consume output
  - Get the final state
  - Multiple types of streaming output, eg. token-by-token, intermediate steps, etc.
  - Able to reconnect to output stream if disconnected
- Handling edge cases
  - Failures should be handled gracefully, and retried if desired
  - Bursty traffic should be queued up

Base Endpoints:

- [`GET /threads/{thread_id}/runs`](https://langchain-ai.github.io/agent-protocol/api.html#tag/background-runs/GET/threads/{thread_id}/runs) - List runs for a thread.
- [`POST /runs`](https://langchain-ai.github.io/agent-protocol/api.html#tag/background-runs/POST/runs) - Create a background run.
- [`GET /runs/{run_id}`](https://langchain-ai.github.io/agent-protocol/api.html#tag/background-runs/GET/runs/{run_id}) - Get a run and its status.
- [`POST /runs/{run_id}/cancel`](https://langchain-ai.github.io/agent-protocol/api.html#tag/background-runs/POST/runs/{run_id}/cancel) - Cancel a run. If the run hasn’t started, cancel it immediately, if it’s currently running then cancel it as soon as possible.
- [`DELETE /runs/{run_id}`](https://langchain-ai.github.io/agent-protocol/api.html#tag/background-runs/DELETE/runs/{run_id}) - Delete a finished run. A pending run needs to be cancelled first, see previous endpoint.
- [`GET /runs/{run_id}/wait`](https://langchain-ai.github.io/agent-protocol/api.html#tag/background-runs/GET/runs/{run_id}/wait) - Wait for a run to finish, return the final output. If the run already finished, returns its final output immediately.
- [`GET /runs/{run_id}/stream`](https://langchain-ai.github.io/agent-protocol/api.html#tag/background-runs/GET/runs/{run_id}/stream) - Join the output stream of an existing run. Only output produced after this endpoint is called will be streamed.

## Store: Long-term memory

What do you need out of a memory API for agents?

- Customizable memory scopes
  - Storing memory against the user, thread, assistant, company, etc
  - Accessing memory from different scopes in the same run
- Flexible storage
  - Support simple text memories, as well as structured data
  - CRUD operations for memories (create, read, update, delete)
- Search and retrieval
  - Get a single memory by namespace and key
  - List memories filtered by namespace, contents, sorted by time, etc

Endpoints:

- [`PUT /store/items`](https://langchain-ai.github.io/agent-protocol/api.html#tag/store/PUT/store/items) - Create or update a memory item, at a given namespace and key.
- [`DELETE /store/items`](https://langchain-ai.github.io/agent-protocol/api.html#tag/store/DELETE/store/items) - Delete a memory item, at a given namespace and key.
- [`GET /store/items`](https://langchain-ai.github.io/agent-protocol/api.html#tag/store/GET/store/items) - Get a memory item, at a given namespace and key.
- [`POST /store/items/search`](https://langchain-ai.github.io/agent-protocol/api.html#tag/store/POST/store/items/search) - Search memory items.
- [`POST /store/namespaces`](https://langchain-ai.github.io/agent-protocol/api.html#tag/store/POST/store/namespaces) - List namespaces.

## Messages

Messages have emerged as a core primitive in dealing with LLMs, and as such we have first-class support for messages in Agent Protocol. This is in addition to completely customizable input/output schemas for agents. We define a Message spec, which is a subset of the message formats supported by major LLM providers, such as OpenAI and Anthropic. In all endpoints that expose thread values, there is also a separate `messages` field, which agents can optionally implement.

## Streaming Primitives

Agent Protocol also defines a thread-centric streaming protocol for observing and controlling live agent executions. The streaming primitives cover transport framing, filtered subscriptions, replay, namespaces for nested agents, content-block message deltas, tool lifecycle events, run lifecycle events, human-in-the-loop input, state snapshots, updates, checkpoints, tasks, and custom events.

The streaming schema and generated bindings live in [`streaming/`](./streaming/). The CDDL schema is the source of truth, with generated TypeScript and Python bindings available for clients and implementations that want strongly typed protocol payloads.

Endpoints:

- [`POST /threads/{thread_id}/stream`](https://langchain-ai.github.io/agent-protocol/api.html#tag/streaming/POST/threads/{thread_id}/stream) - Open a filtered Server-Sent Events stream for a thread. The request body selects channels, namespace prefixes, optional depth, and optional replay position.
- [`GET /threads/{thread_id}/stream`](https://langchain-ai.github.io/agent-protocol/api.html#tag/streaming/GET/threads/{thread_id}/stream) - Upgrade to a WebSocket connection for bidirectional streaming. Once upgraded, commands, command responses, and unsolicited events share the same connection.
- [`POST /threads/{thread_id}/commands`](https://langchain-ai.github.io/agent-protocol/api.html#tag/streaming/POST/threads/{thread_id}/commands) - Send a streaming protocol command over HTTP and receive the correlated command response. This is the command sidecar for SSE clients; WebSocket clients send commands in-band.

## Agent Protocol in Action

Below are a few illustrative “user journeys” in [Hurl](https://hurl.dev) format, each showing a common sequence of API calls against your Agent Protocol service (listening at localhost:8000, no auth required).

They’re organized so that you can paste each journey into its own .hurl file (or combine them), then run them with the “hurl” command. This should give you a good sense of how the protocol can be used in practice.

### Journey 1: Create Thread → Get Thread → Create Run → Wait for Output

This journey demonstrates the typical sequence of creating a thread, launching a run, and waiting for the final output. You can then repeat the two last steps to launch more runs in the same thread. This is the most common pattern for multi-turn interactions, such as a chatbot conversation.

```hurl
# 1. Create a brand new thread
POST http://localhost:8000/threads
Content-Type: application/json

{
  "thread_id": "229c1834-bc04-4d90-8fd6-77f6b9ef1462",
  "metadata": {
    "purpose": "support-chat"
  }
}

HTTP/1.1 200
[Asserts]
jsonpath "$.thread_id" == "229c1834-bc04-4d90-8fd6-77f6b9ef1462"


# 2. Retrieve the thread we just created
GET http://localhost:8000/threads/229c1834-bc04-4d90-8fd6-77f6b9ef1462

HTTP/1.1 200
[Asserts]
jsonpath "$.status" == "idle"


# 3. Create a run in the existing thread (background run).
# Capture the run_id for the next step.
POST http://localhost:8000/threads/229c1834-bc04-4d90-8fd6-77f6b9ef1462/runs
Content-Type: application/json

{
  "input": {
    "message": "Hi there, what's the weather?"
  },
  "metadata": {
    "requestType": "weatherQuery"
  }
}

HTTP/1.1 200
[Captures]
run_id: jsonpath "$.run_id"
[Asserts]
jsonpath "$.status" == "pending"


# 4. Wait for final run output
GET http://localhost:8000/threads/229c1834-bc04-4d90-8fd6-77f6b9ef1462/runs/{{run_id}}/wait

HTTP/1.1 200
[Asserts]
# For example, check that the run status is success or error,
# depending on your actual system's response:
jsonpath "$.status" == "success"
```

You can replace the last step with `GET /threads/{thread_id}/runs/{run_id}/stream` to stream the output as it’s produced, or with `GET /threads/{thread_id}` to poll status/output without waiting.

### Journey 2: Ephemeral “Stateless” Run (Create + Wait)

This journey demonstrates a one-shot run, where you create a thread and run in one request, and wait for the final output. This is useful for stateless interactions, where you want to start fresh each time. Good use cases include extraction or research agents.

```hurl
# Launch a one-shot run with a brand new ephemeral thread,
# and wait for the final output right away.
POST http://localhost:8000/runs/wait
Content-Type: application/json

{
  "input": {
    "prompt": "What's the fastest route to the airport?"
  },
  "metadata": {
    "useCase": "travelPlan"
  },
  "config": {
    "tags": ["ephemeral", "demo"]
  }
}

HTTP/1.1 200
```

### Journey 3: Using the Store (Add, Retrieve, and Delete an Item)

This journey demonstrates how to use the Store API to add, retrieve, and delete an item. This is useful for storing long-term memory, such as user profiles, preferences, or other structured data, which can be accessed both inside and outside the agent.

```hurl
# 1. Put (store or update) an item in the store
PUT http://localhost:8000/store/items
Content-Type: application/json

{
  "namespace": ["user_profiles"],
  "key": "profile_jane_doe",
  "value": {
    "displayName": "Jane Doe",
    "role": "customer"
  }
}

HTTP/1.1 204


# 2. Retrieve it by namespace/key
GET http://localhost:8000/store/items?key=profile_jane_doe&namespace=user_profiles

HTTP/1.1 200
[Asserts]
jsonpath "$.value.displayName" == "Jane Doe"
jsonpath "$.value.role" == "customer"


# 3. Delete the item
DELETE http://localhost:8000/store/items
Content-Type: application/json

{
  "namespace": ["user_profiles"],
  "key": "profile_jane_doe"
}

HTTP/1.1 204
```

## Roadmap

- Add detailed specification for each stream mode (currently this is left open to the implementer)
- Add Store endpoint to perform a vector search over memory entries
- Add param for `POST /threads/{thread_id}/runs/{run_id}/stream` to replay events since `event-id` before streaming new events
- Add param to `POST /threads/{thread_id}/runs` to optionally allow concurrent runs on the same thread (current spec makes this forbidden)
- (Open an issue and let us know what else should be here!)
