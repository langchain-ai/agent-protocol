# Agent Protocol

Agent Protocol is our attempt at codifying the framework-agnostic APIs that are needed to serve LLM agents in production. This document explains the purpose of the protocol and makes the case for each of the endpoints in the spec. We finish by listing some roadmap items for the future.

See the full OpenAPI docs [here](https://langchain-ai.github.io/agent-protocol/api.html) and the JSON spec [here](https://langchain-ai.github.io/agent-protocol/openapi.json).

[LangGraph Platform](https://www.langchain.com/pricing-langgraph-platform) implements a superset of this protocol, but we very much welcome other implementations from the community.

## Why Agent Protocol

What is the right API to serve an LLM application in production? We believe it’s centered around 3 important concepts:

- Runs: APIs for executing an agent
- Threads: APIs to organize multi-turn executions of agents
- Store: APIs to work with long-term memory

Let’s dive deeper into each one, starting with the requirements, and then presenting the Protocol endpoints that meet these requirements.

## Runs: Atomic agent executions

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

- [`GET /threads/{thread_id}/runs`](https://langchain-ai.github.io/agent-protocol/api.html#tag/runs/GET/threads/%7Bthread_id%7D/runs) - List runs.
- [`POST /threads/{thread_id}/runs`](https://langchain-ai.github.io/agent-protocol/api.html#tag/runs/POST/threads/%7Bthread_id%7D/runs) - Create a run.
- [`GET /threads/{thread_id}/runs/{run_id}`](https://langchain-ai.github.io/agent-protocol/api.html#tag/runs/GET/threads/%7Bthread_id%7D/runs/%7Brun_id%7D) - Get a run and its status.
- [`POST /threads/{thread_id}/runs/{run_id}/cancel`](https://langchain-ai.github.io/agent-protocol/api.html#tag/runs/POST/threads/%7Bthread_id%7D/runs/%7Brun_id%7D/cancel) - Cancel a run. If the run hasn’t started, cancel it immediately, if it’s currently running then cancel it as soon as possible.
- [`DELETE /threads/{thread_id}/runs/{run_id}`](https://langchain-ai.github.io/agent-protocol/api.html#tag/runs/DELETE/threads/%7Bthread_id%7D/runs/%7Brun_id%7D) - Delete a finished run. A pending run needs to be cancelled first, see previous endpoint.
- [`GET /threads/{thread_id}/runs/{run_id}/wait`](https://langchain-ai.github.io/agent-protocol/api.html#tag/runs/GET/threads/%7Bthread_id%7D/runs/%7Brun_id%7D/wait) - Wait for a run to finish, return the final output. If the run already finished, returns its final output immediately.
- [`GET /threads/{thread_id}/runs/{run_id}/stream`](https://langchain-ai.github.io/agent-protocol/api.html#tag/runs/GET/threads/%7Bthread_id%7D/runs/%7Brun_id%7D/stream) - Join the output stream of an existing run. Only output produced after this endpoint is called will be streamed.

Convenience Endpoints:

- [`POST /threads/{thread_id}/runs/wait`](https://langchain-ai.github.io/agent-protocol/api.html#tag/runs/POST/threads/%7Bthread_id%7D/runs/wait) - Create a run, and wait for its final output.
- [`POST /threads/{thread_id}/runs/stream`](https://langchain-ai.github.io/agent-protocol/api.html#tag/runs/POST/threads/%7Bthread_id%7D/runs/stream) - Create a run, and stream output as produced.
- [`POST /threads/runs`](https://langchain-ai.github.io/agent-protocol/api.html#tag/runs/POST/threads/runs) - Create a ephemeral thread and run in one request. The thread will be deleted after the run concludes.
- [`POST /threads/runs/wait`](https://langchain-ai.github.io/agent-protocol/api.html#tag/runs/POST/threads/runs/wait) - Create a ephemeral thread and run, and wait for its final output.
- [`POST /threads/runs/stream`](https://langchain-ai.github.io/agent-protocol/api.html#tag/runs/POST/threads/runs/stream) - Create a ephemeral thread and run, and stream output as produced.

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
- [`GET /threads/{thread_id}/state`](https://langchain-ai.github.io/agent-protocol/api.html#tag/threads/GET/threads/%7Bthread_id%7D/state) - Get the latest state of a thread.
- [`POST /threads/{thread_id}/state`](https://langchain-ai.github.io/agent-protocol/api.html#tag/threads/POST/threads/%7Bthread_id%7D/state) - Create a new revision of the thread’s state.
- [`GET /threads/{thread_id}/history`](https://langchain-ai.github.io/agent-protocol/api.html#tag/threads/GET/threads/%7Bthread_id%7D/history) - Browse past revisions of a thread’s state. Revisions are created by runs, or through the endpoint just above.
- [`POST /threads/{thread_id}/copy`](https://langchain-ai.github.io/agent-protocol/api.html#tag/threads/POST/threads/%7Bthread_id%7D/copy) - Create an independent copy of a thread.
- [`DELETE /threads/{thread_id}`](https://langchain-ai.github.io/agent-protocol/api.html#tag/threads/DELETE/threads/%7Bthread_id%7D) - Delete a thread.
- [`PATCH /threads/{thread_id}`](https://langchain-ai.github.io/agent-protocol/api.html#tag/threads/PATCH/threads/%7Bthread_id%7D) - Update the metadata for a thread.

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

## Roadmap

- Add Store endpoint to perform a vector search over memory entries
- Add param for `POST /threads/{thread_id}/runs/{run_id}/stream` to replay events since `event-id` before streaming new events
- Add param to `POST /threads/{thread_id}/runs ` to optionally allow concurrent runs on the same thread (current spec makes this forbidden)
- (Open an issue and let us know what else should be here!)
