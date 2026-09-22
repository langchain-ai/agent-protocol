# Agent Protocol compared with A2A and Open Responses

Agent Protocol, [A2A (Agent2Agent)](https://a2a-protocol.org/latest/specification/) and [Open Responses](https://www.openresponses.org/specification) are frequently mentioned together, and all three describe HTTP APIs for talking to LLM-driven systems. They are not competing answers to the same question. Each one standardises a different relationship between a client and an LLM system, and the differences in their data models follow directly from that.

This document explains what each protocol is for, how their core concepts map onto one another, and where they genuinely differ. It is written from the perspective of Agent Protocol, but aims to describe the other two fairly and on their own terms.

## The one-paragraph version

- **Open Responses** standardises the interface between an application and a **model**. It is a vendor-neutral specification of the OpenAI Responses API shape: the client sends a list of input items and tool definitions, the model returns output items (messages, reasoning, tool calls), and the client runs the agentic loop by executing tool calls and sending the results back. It is the layer an agent is *built on*.
- **Agent Protocol** standardises the interface between an application or platform and a **deployed agent runtime**. The client is trusted: it can create threads, start, stream, cancel and resume runs, read and edit persisted state, walk checkpoint history, fork from a checkpoint, and read and write long-term memory. It is the layer an agent is *served through*.
- **A2A** standardises the interface between one agent and **another, opaque agent**, often across organisational boundaries. The client discovers the remote agent through an Agent Card, sends it messages, and receives tasks with status updates and artifacts. By design it does not expose the remote agent's internal state, memory or tools. It is the layer agents *talk to each other over*.

A single system can implement all three at once: it can call models through Open Responses, be operated by its own UI through Agent Protocol, and be exposed to third-party agents through A2A.

## At a glance

| | Agent Protocol | A2A | Open Responses |
| --- | --- | --- | --- |
| Governance | LangChain, open source (MIT) | Linux Foundation project (Apache-2.0) | Initiated by OpenAI with launch partners, maintained in the open (Apache-2.0) |
| Current version | OpenAPI spec 0.1.6; streaming schema 0.0.13 (draft) | 1.0 | Dated releases; latest is 2026-04-24 |
| Relationship standardised | Application or platform to agent runtime | Agent to peer agent | Application to model provider |
| Is the server opaque to the client? | No. State, history, checkpoints and memory are all readable and writable | Yes, deliberately | Mostly. The client holds the transcript; the server holds at most a chain of stored responses |
| Unit of execution | Run (on a thread, or ephemeral) | Task (within a context) | Response |
| Multi-turn container | Thread | `contextId` | `previous_response_id` chain, or a client-held transcript |
| Content model | Messages with content blocks; arbitrary JSON state | Messages and Artifacts made of Parts | Items (message, function_call, function_call_output, reasoning) with content parts |
| Wire format | REST/JSON described in OpenAPI; SSE; WebSocket; CDDL for streaming payloads | JSON-RPC 2.0, gRPC, and HTTP+JSON bindings over a Protocol Buffers data model | HTTP POST with SSE; WebSocket |
| Streaming granularity | Content-block deltas, tool lifecycle, state updates, checkpoints, per-namespace | Task status and artifact update events | Semantic `response.*` events, including text and argument deltas |
| Human in the loop | `interrupted` run status; `input.requested` / `input.respond` on the stream | `input-required` and `auth-required` task states | None as such. A client-side tool call pauses the loop |
| Discovery | `/agents/search`, `/agents/{id}`, `/agents/{id}/schemas` | Agent Card at a well-known URL, with skills, capabilities and security schemes | None. The `model` field names the target |
| Long-term memory | Store endpoints (namespaced key-value with search) | Out of scope | Out of scope |
| Tool calling | Tools are internal to the agent and observable on the stream | Tools are hidden behind the agent | Tools are the core of the API; the client defines and executes them |
| Authentication | Not specified | Declared per agent in the Agent Card using standard HTTP schemes | `Authorization` header |
| Extension mechanism | Custom capabilities in reverse-domain notation, `custom:*` stream channels, open content block types | Extensions declared by URI in the Agent Card | Implementor-slug prefixes on item, event and tool types (for example `acme:search_result`) |

## What each protocol is for

### Agent Protocol: serving an agent in production

Agent Protocol assumes a trusted client. The typical caller is the application's own front end, a backend orchestrator, or a platform operating the agent on someone's behalf. Such a caller needs to do much more than send a message and wait for an answer:

- Organise multi-turn interactions into **threads**, list and search them by metadata or status, copy them, and delete them.
- Read the **current state** of a thread, patch it, and walk its **history** as an append-only log of checkpoints.
- Start **runs** on a thread with control over waiting, streaming, running in the background, cancellation, webhooks, and behaviour when a run is already active on the thread.
- Resume a run that has stopped for human input.
- Read and write **long-term memory** in a namespaced store, independent of any single thread.
- Introspect the agent's **input, output, state and config schemas**.

None of this makes sense if the agent is a black box, so Agent Protocol does not treat it as one. The streaming protocol goes further and exposes the internal structure of the agent: events carry a **namespace** identifying which nested subagent or subgraph produced them, and clients can subscribe to the whole tree, a single branch, or a bounded depth.

### A2A: letting independent agents collaborate

A2A starts from the opposite assumption. The remote agent may belong to a different team, company or vendor, and the protocol is explicit that agents collaborate "without needing access to each other's internal state, memory, or tools". The client is itself usually an agent.

That assumption shapes everything else:

- **Discovery is first class.** An Agent Card describes the agent's skills, supported input and output modes, transport endpoints, optional capabilities (streaming, push notifications, state transition history), and security schemes. Cards can be signed, and an authenticated client can fetch an extended card with more detail.
- **The unit of work is a Task**, which the server creates and owns. A task moves through `submitted`, `working`, `input-required`, `auth-required`, `completed`, `failed`, `canceled` or `rejected`. Outputs are **Artifacts** made of Parts, kept separate from the status messages exchanged along the way.
- **Multi-turn is loose.** A `contextId` groups related tasks and messages; the client may supply one or accept a server-generated one. A client continues an interaction by sending a message that references the existing task or context, not by editing state.
- **Delivery is async-first.** Clients can poll with `GetTask`, stream with `SendStreamingMessage` or `SubscribeToTask`, or register a webhook for push notifications, which matters when a task may run for hours.

A2A intentionally says nothing about how the agent reasons, what tools it has, or how it stores memory. Those are the remote agent's business.

### Open Responses: a common shape for model APIs

Open Responses is a different kind of specification again. It is not an API for calling a deployed agent; it is a vendor-neutral write-up of the OpenAI Responses API, so that a request written once can be served by OpenAI, a gateway, a local inference server or another provider. It was announced by OpenAI in January 2026 with launch partners including OpenRouter, Hugging Face, Ollama, vLLM, LM Studio and Vercel.

Its primitives are those of a model call:

- A **Response** is created by `POST /v1/responses` with a `model`, an `input` list of items, optional `tools`, `tool_choice` and `allowed_tools`, and optionally `previous_response_id` to continue a stored chain.
- **Items** are the atomic unit of context. The standard types are `message`, `function_call`, `function_call_output` and `reasoning`; every item has an `id`, `type` and `status`. Providers add their own item types under a slug prefix, such as `openai:web_search_call`.
- **The agentic loop lives on the client.** When the model emits a `function_call`, control returns to the caller, which executes the function and sends a `function_call_output` item in the next request. Provider-hosted tools are the exception: the provider runs them and keeps control until the model finishes.
- **Streaming is semantic.** Rather than a bare token stream, the server emits typed events such as `response.output_item.added`, `response.output_text.delta`, `response.function_call_arguments.delta` and `response.completed`, each carrying a `sequence_number`.
- **State is thin.** `store` controls whether the response is persisted, `previous_response_id` continues a stored chain without resending it, and a `compact` endpoint returns a shortened input window when a chain can no longer be continued. There is no readable state object beyond the responses themselves.

An agent framework typically sits *above* Open Responses, using it to talk to models, and *below* Agent Protocol or A2A, which expose the resulting agent to callers.

## Concept mapping

The rough correspondences below are useful for orientation. None of them is exact, and the notes explain where they break down.

| Agent Protocol | A2A | Open Responses | Notes |
| --- | --- | --- | --- |
| Agent (`agent_id`) | Agent Card | `model` | Agent Protocol and A2A describe a deployed agent; Open Responses names a model. Agent Protocol exposes JSON schemas for input, output, state and config; A2A exposes skills and modes; Open Responses exposes neither. |
| Thread | `contextId` | `previous_response_id` chain | A thread is a durable object with state, status and history. A `contextId` is a grouping key with no state of its own. A response chain is server-side storage of the transcript, if `store` is enabled. |
| Run | Task | Response | A run executes an agent once on a thread. A task is a server-owned unit of work that may span multiple message exchanges. A response is one model turn; a client loop over several responses is what an Agent Protocol run does internally. |
| Run status: `pending`, `success`, `error`, `timeout`, `interrupted` | Task state: `submitted`, `working`, `input-required`, `auth-required`, `completed`, `failed`, `canceled`, `rejected` | Response status: `queued`, `in_progress`, `completed`, `failed`, `incomplete` | Only A2A distinguishes an agent refusing a task (`rejected`) or needing credentials (`auth-required`). Only Open Responses has a terminal state for running out of token budget (`incomplete`). |
| Message with content blocks | Message with Parts | `message` item with content parts | All three use a role plus a list of typed content parts. Agent Protocol's block set matches LangChain content blocks and includes reasoning, tool calls and multimodal data. A2A Parts are text, file or data. Open Responses distinguishes input content types from output content types. |
| Tool call content block; `tools` stream channel | Not exposed | `function_call` and `function_call_output` items | Agent Protocol lets the client observe tool calls the agent makes. A2A hides them. Open Responses makes the client responsible for executing them. |
| Thread state, checkpoints, `state.fork` | Not exposed (task history and artifacts only) | Not exposed | This is the sharpest difference. Agent Protocol treats state, history and time travel as part of the API; the other two treat them as implementation details. |
| Store items | Out of scope | Out of scope | Agent Protocol is the only one of the three with a long-term memory API. |
| Interrupt: `interrupted` status, `input.requested` event, `input.respond` command | `input-required` state, then another `SendMessage` on the task | A `function_call` awaiting `function_call_output` | Agent Protocol's resume can also carry a state update and a jump to a named node in the same step. |
| Webhook on run completion | Push notification config per task | `background` responses (outside the WebSocket binding) | A2A's webhook registration is a full CRUD resource. Agent Protocol's is a URL on the run request. |
| Stream namespaces for nested agents | Not modelled | Not modelled | A2A composes agents by having one agent call another over A2A; the nesting is invisible to the original caller. Open Responses has a single response scope. |

## Detailed differences

### Who the client is, and how much it is trusted

This is the root difference and the one to keep in mind when reading the rest.

Agent Protocol's client is an operator of the agent. It can see and change anything the agent persists. That is why the protocol has `GET /threads/{thread_id}/history`, `PATCH /threads/{thread_id}`, `POST /threads/{thread_id}/copy`, checkpoint events, and a fork command. It is also why the protocol does not specify authentication: the deployment is expected to sit behind whatever gate the operator already has.

A2A's client is a peer, possibly one the agent has never met. Authentication is therefore declared per agent, capability flags tell the client what it is allowed to expect, and nothing about the agent's internals leaks across the boundary. If the remote agent is itself built on LangGraph and served through Agent Protocol, none of that is visible over A2A, and that is the point.

Open Responses' client is an application developer holding the transcript. The server is a stateless function from context to output items, with optional convenience storage of previous responses. Trust is a bearer token in the `Authorization` header and nothing more is said.

### Where the agentic loop runs

In Open Responses the loop is the client's job. The model proposes a tool call; the client executes it and reports back. This is what makes the specification portable across model providers, and it is also why an Open Responses endpoint is not by itself an agent API: an agent that exposes only `POST /v1/responses` is asking its caller to run its tools.

In Agent Protocol and A2A the loop runs on the server. The client starts a run or task and the agent decides which tools to call and calls them. The two differ in what the client can see while that happens. Agent Protocol streams every tool call, tool result and intermediate state change, with a namespace so the client knows which subagent did what. A2A reports task status transitions and artifacts and nothing about how they were produced.

### Multi-turn state

Agent Protocol makes the thread a durable, first-class object. Each run appends checkpoints to the thread's history, the current state can be read and patched between runs, and a run can be started from an earlier checkpoint to branch the conversation. The protocol also mandates that only one run is active per thread at a time, which is what makes state reads and writes well defined.

A2A's `contextId` is a correlation key. It lets a client and agent agree that several tasks belong to the same conversation, and the agent may use it to recall earlier tasks, but the protocol defines no state object for the context and no way to read or edit one. What the client can retrieve is the task history and artifacts, optionally trimmed with a history length parameter.

Open Responses stores individual responses. Setting `previous_response_id` tells the server to prepend the earlier input and output before the new input, so the client does not resend them. Nothing is readable beyond the responses themselves, and with `store` set to false the chain exists only for the life of a WebSocket connection. The `compact` endpoint exists precisely because there is no server-side state to fall back on when the chain grows too long.

### Streaming

All three stream over Server-Sent Events in their HTTP bindings, and Agent Protocol and Open Responses also define WebSocket bindings. The differences are in what is streamed and how the stream is structured.

Agent Protocol has two layers. The run-level endpoints stream in one or more modes (`values`, `messages`, `updates`, `custom`). The thread-level streaming protocol, defined in CDDL under `streaming/`, adds a richer model: clients subscribe to **channels** (`messages`, `tools`, `lifecycle`, `input`, `values`, `updates`, `checkpoints`, `tasks`, `custom`), filter by **namespace** prefix and depth, and reconnect with a sequence number to replay missed events. Model output streams as content blocks with explicit `message-start`, `content-block-start`, `content-block-delta`, `content-block-finish` and `message-finish` boundaries, and delta types with defined append or merge semantics. Multiple clients can observe the same thread with different filters, and over WebSocket the same connection carries commands such as `run.start`, `input.respond` and `state.fork`.

A2A streams at the granularity of the task. `SendStreamingMessage` and `SubscribeToTask` deliver task status update events and artifact update events, and an artifact can be delivered in chunks that the client appends. There is no first-class representation of model tokens, reasoning or tool calls in flight, because those belong to the opaque interior. The gRPC binding uses server streaming for the same events, and push notifications deliver the same status changes to a webhook when no connection is open.

Open Responses streams semantic events for a single response: item added, content part added, text delta, function-call argument delta, item done, and the response lifecycle events (`queued`, `in_progress`, `completed`, `failed`). Every event carries a `sequence_number`. The structure is close to Agent Protocol's `messages` channel, which is not a coincidence: both mirror how model providers stream today. What Open Responses lacks is anything above the single response: no channels, no namespaces, no state or checkpoint events, and no replay across connections.

### Human in the loop

Agent Protocol models an interrupt as a state of the run and thread (`interrupted`), with the pending request delivered as an `input.requested` event carrying an interrupt ID and an application-defined payload. The client answers with `input.respond`, and can attach a state update and a jump target so that the resume, the update and the redirect land in a single checkpoint. A resumed run continues from where it stopped.

A2A models the same situation as the `input-required` task state, and adds `auth-required` for the case where the agent needs the user to authenticate with some third party before it can continue. The client continues the task by sending another message that references it. There is no separate resume verb, and no way to attach a state change, because there is no exposed state.

Open Responses has no concept of an interrupt. A client-side function call pauses the loop, and a human can be consulted before the `function_call_output` is sent, but the protocol does not know the difference between a tool that took a while and a person who was asked a question.

### Discovery and capabilities

Agent Protocol's discovery is aimed at a client that already knows which deployment it is talking to. `POST /agents/search` lists agents, `GET /agents/{agent_id}` returns one with its capabilities, and `GET /agents/{agent_id}/schemas` returns JSON schemas for input, output, state and config. Capabilities are a flat map: the standard ones are `ap.io.messages` and `ap.io.streaming`, and implementations add their own in reverse-domain notation.

A2A's Agent Card is designed for a client that has only a URL. It carries a human-readable description, a list of skills with examples, default input and output modes, the transports and endpoints the agent supports, capability flags, security schemes, and the protocol version. It is published at a well-known path, can be signed, and can have an authenticated extended version. Discovery is a core part of A2A in a way it is not for the other two.

Open Responses has no discovery. The `model` field names the target and the provider's own documentation says what it supports. Provider discovery is explicitly out of scope.

### Memory

Agent Protocol includes a Store: items are addressed by a namespace tuple and a key, can hold arbitrary JSON, and can be searched and listed by namespace. This lets the same memory be scoped to a user, an organisation or an agent and shared across threads.

Neither A2A nor Open Responses has a memory API. In A2A memory is inside the opaque agent. In Open Responses it is the client's transcript or, at most, the stored response chain.

### Transports and schema languages

Agent Protocol is REST over HTTP with JSON bodies, described in an OpenAPI document that is the source of truth for the spec. Streaming uses SSE, with a WebSocket upgrade on the thread stream endpoint. The streaming payloads are specified in CDDL, from which TypeScript and Python bindings are generated.

A2A defines a canonical data model in Protocol Buffers and then three bindings over it: JSON-RPC 2.0 over HTTP, gRPC, and HTTP+JSON with REST conventions. An agent advertises which bindings it supports in its card, and clients send an `A2A-Version` header.

Open Responses is a single HTTP endpoint with SSE for streaming, plus a WebSocket binding at the same path for long-lived multi-turn sessions, described in OpenAPI.

### Extensibility

Agent Protocol extends through open-ended JSON: agent capabilities in reverse-domain notation, arbitrary thread and run metadata, a `MessageAnyBlock` content type and a non-standard content block escape hatch, and `custom:*` stream channels for application events.

A2A has a formal extension mechanism: extensions are identified by URI, listed in the Agent Card, can be marked required, and are negotiated through an `A2A-Extensions` service parameter.

Open Responses reserves namespaced names: any custom item, event or tool type must be prefixed with an implementor slug, so `openai:web_search_call` and `acme:search_result` cannot collide and their ownership is clear in logs.

## How they fit together

Because the three protocols standardise different boundaries, the practical question is rarely "which one" but "which one at which boundary".

- **Calling a model:** Open Responses. An agent implemented with any framework can use it to reach whichever provider serves the model, and swap providers without rewriting the loop.
- **Operating your own agent:** Agent Protocol. A front end, an evaluation harness or an orchestrator that needs threads, streaming with subagent visibility, interrupts, time travel and memory gets all of that from one API.
- **Exposing an agent to other agents:** A2A. A partner's orchestrator needs to discover the agent, authenticate, hand it work and get artifacts back, and needs to be shielded from the agent's internals.

Mapping between the outer two is straightforward at the level of concepts. An Agent Protocol server can be fronted by an A2A adapter that maps a `contextId` to a thread, a task to a run, an `interrupted` run to `input-required`, the thread's final messages to artifacts, and the run webhook to push notifications. What such an adapter deliberately drops is everything A2A treats as private: state reads and writes, checkpoints, subagent namespaces and the store.

## References

- Agent Protocol: [README](../README.md), [OpenAPI spec](../openapi.json), [streaming protocol](../streaming/README.md)
- A2A: [specification](https://a2a-protocol.org/latest/specification/), [What is A2A](https://a2a-protocol.org/latest/topics/what-is-a2a/)
- Open Responses: [specification](https://www.openresponses.org/specification), [repository](https://github.com/openresponses/openresponses)
