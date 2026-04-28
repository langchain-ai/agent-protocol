# Agent Streaming Protocol

This directory contains the Agent Protocol streaming specification and generated
language bindings:

- `protocol.cddl`: the source of truth for the wire format.
- `js/`: generated TypeScript types for protocol payloads.
- `py/`: generated Python `TypedDict` and `Literal` types for protocol payloads.

The streaming protocol is a thread-centric event and command protocol for
observing and controlling long-running agent executions. It is designed for
multiple transports, supports filtered subscriptions, and makes streamed model
output, tool activity, graph state, checkpoints, lifecycle status, and
human-in-the-loop interactions available through a common envelope.

## Design Goals

The protocol is built around a few stable primitives:

- Threads are the durable routing key for commands, events, state, checkpoints,
  and run history.
- Connections are ephemeral transport scopes. Multiple clients can observe the
  same thread concurrently with different filters.
- Channels partition the event stream by concern, so clients can subscribe only
  to the data they need.
- Namespaces identify positions in an agent or graph tree, allowing clients to
  subscribe to a root agent, a subgraph, or a bounded depth below either.
- Content blocks are the universal carrier for model output deltas, including
  text, reasoning, tool calls, server-side tool calls, multimodal data, and
  provider-specific extensions.
- Events carry explicit lifecycle boundaries. Clients do not need to infer when
  a message, content block, tool call, run, or subgraph starts and finishes.
- Replay is sequence-based, allowing clients to reconnect and request missed
  events from the server's event buffer.

## Transport Model

The CDDL schema defines a single payload model that can be used over SSE/HTTP,
WebSocket, and in-process transports.

### SSE/HTTP

SSE uses connection-scoped subscriptions:

- `POST /v2/threads/:thread_id/events` opens a filtered event stream.
- `POST /v2/threads/:thread_id/commands` sends a JSON command and receives a
  JSON response.

The `events` request body is an `EventStreamRequest`:

```json
{
  "channels": ["messages", "updates", "lifecycle"],
  "namespaces": [[]],
  "depth": 2,
  "since": 123
}
```

Each SSE connection is its own subscription. Closing the connection unsubscribes
from that stream. A client may open multiple event streams for the same thread,
for example one stream for low-latency model tokens and another for state or
checkpoint updates.

### WebSocket

WebSocket uses in-band commands over a single full-duplex connection:

- `subscription.subscribe` creates a filtered subscription.
- `subscription.unsubscribe` removes a subscription.
- `subscription.reconnect` restores subscriptions and requests missed events.

Subscriptions persist across run boundaries and are removed explicitly or when
the WebSocket closes.

## Top-Level Framing

Client-to-server messages are commands:

```json
{
  "id": 1,
  "method": "run.input",
  "params": {
    "assistantId": "agent",
    "input": {
      "messages": [{ "role": "user", "content": "Hello" }]
    }
  }
}
```

Server-to-client messages are either command responses, error responses, or
events.

Successful responses include the original command `id` and a typed `result`:

```json
{
  "type": "success",
  "id": 1,
  "result": {
    "runId": "run_123"
  },
  "meta": {
    "appliedThroughSeq": 42
  }
}
```

Error responses include the original command `id` when available:

```json
{
  "type": "error",
  "id": 1,
  "error": "invalid_argument",
  "message": "assistantId is required"
}
```

Events are unsolicited server pushes:

```json
{
  "type": "event",
  "eventId": "evt_123",
  "seq": 43,
  "method": "messages",
  "params": {
    "namespace": [],
    "timestamp": 1710000000000,
    "data": {
      "event": "message-start",
      "role": "ai",
      "id": "msg_123"
    }
  }
}
```

The optional `eventId` maps to the SSE `id:` field and is used for transport
reconnection. The optional `seq` is a monotonic sequence number used for
ordering and replay.

## Threads, Runs, and Input

The protocol is thread-centric. A thread is the durable identity for state,
checkpoints, run history, and stream routing. A server may create a thread
lazily when it receives the first `run.input` command for a thread that does not
exist yet.

`run.input` is the main entry point for execution input:

- If no run is active, it starts a new run.
- If the run is interrupted, it resumes the run with the provided value.
- If a run is active, it injects input into the running graph.

The command carries the target `assistantId`, arbitrary graph input, optional
runtime config, and optional metadata.

Human-in-the-loop control uses the input module:

- `input.requested` events ask the client for a response to an interrupt.
- `input.respond` sends a response correlated by `interruptId`.
- `input.inject` sends unsolicited user or system input into a namespace.

## Namespaces

A namespace is a path of strings identifying a location in the agent tree:

- `[]` identifies the root agent or graph.
- `["researcher"]` identifies a direct child.
- `["supervisor", "worker_a"]` identifies a nested child.

Subscriptions can filter by namespace prefix and optional depth. This allows a
client to observe the whole tree, a single subgraph, or a bounded region under a
subgraph without receiving unrelated events.

## Channels

Channels are the primary subscription unit. A client requests one or more
channels and receives only matching events.

### `messages`

The `messages` channel streams transcript messages and content blocks. It uses
explicit event boundaries:

1. `message-start`
2. `content-block-start`
3. zero or more `content-block-delta` events
4. `content-block-finish`
5. repeat content block events for additional blocks
6. `message-finish`

Content blocks do not interleave within a single message. Block `N` finishes
before block `N + 1` starts. This matches common LLM provider streaming behavior
and keeps client assembly deterministic.

Delta events carry the same content block union as finalized content. The
block's `type` field is the discriminant. For example:

```json
{
  "event": "content-block-delta",
  "index": 0,
  "content": {
    "type": "text",
    "text": "Hello "
  }
}
```

Tool call arguments stream as chunk content and finalize as parsed tool calls:

```json
{
  "event": "content-block-delta",
  "index": 1,
  "content": {
    "type": "tool_call_chunk",
    "id": "call_123",
    "name": "search",
    "args": "{\"query\":"
  }
}
```

```json
{
  "event": "content-block-finish",
  "index": 1,
  "content": {
    "type": "tool_call",
    "id": "call_123",
    "name": "search",
    "args": {
      "query": "weather"
    }
  }
}
```

`message-finish` may include token usage for AI-authored messages.
Unrecoverable model-call failures are emitted as message `error` events.

### `tools`

The `tools` channel exposes tool execution lifecycle observability:

1. `tool-started`
2. zero or more `tool-output-delta` events for streaming tools
3. `tool-finished` or `tool-error`

Tool events are correlated by `toolCallId`. Clients can connect a tool execution
back to a tool call content block by matching the tool call content block `id`
with `toolCallId`.

### `lifecycle`

The `lifecycle` channel tracks root run and subgraph status:

- `started`
- `running`
- `completed`
- `failed`
- `interrupted`

Lifecycle events include a `namespace`, optional `graphName`, optional `error`,
optional `checkpoint`, and optional `cause`.

The `cause` field explains why a child namespace started. Current cause variants
include:

- `toolCall`: a parent tool call spawned the child graph.
- `send`: a parent graph used a fan-out send primitive.
- `edge`: a graph edge transitioned into a child graph.

Consumers should tolerate unknown cause types so new cause variants can be added
without breaking existing clients.

### `input`

The `input` channel carries human-in-the-loop requests. An `input.requested`
event contains an `interruptId` and application-defined `payload`. Clients
answer with `input.respond`, passing the same namespace and interrupt ID.

### `values`

The `values` channel carries full graph state snapshots. When a subscription is
created, the first replayed `values` event is the current full state, giving the
client a stable baseline before applying deltas from other channels.

### `updates`

The `updates` channel carries per-node or per-step state deltas:

```json
{
  "method": "updates",
  "params": {
    "namespace": [],
    "timestamp": 1710000000000,
    "data": {
      "node": "agent",
      "values": {
        "messages": []
      }
    }
  }
}
```

Clients that need complete state should subscribe to `values` for an initial
snapshot and use `updates` for incremental changes.

### `checkpoints`

The `checkpoints` channel emits lightweight checkpoint envelopes. Each envelope
includes:

- `id`: the fork target for `state.fork`.
- `parentId`: optional parent checkpoint ID for tree reconstruction.
- `step`: superstep number.
- `source`: one of `input`, `loop`, `update`, or `fork`.

This lets clients build branching and time-travel interfaces without streaming
full checkpoint state. Full state can be fetched lazily with `state.get` or in
bulk with `state.listCheckpoints`.

A checkpoint event is emitted on the same superstep as the corresponding
`values` event. Clients subscribed to both can correlate them by namespace and
step, or by adjacent event sequence numbers.

### `tasks`

The `tasks` channel carries Pregel task creation and result events. Its payload
shape is intentionally open because it follows the runtime task representation.

### `custom` and `custom:*`

The `custom` channel carries user-defined payloads emitted from graph code. The
base `custom` channel uses a `name` and `payload` envelope. Namespaced custom
channels such as `custom:progress` allow applications to define more specific
event lanes while keeping the protocol extensible.

## State and Checkpoints

The state module provides command-level access to graph state:

- `state.get` reads current state values for a namespace, optionally restricted
  to selected keys.
- `state.listCheckpoints` lists checkpoint summaries, optionally scoped to a
  namespace.
- `state.fork` starts a run from a checkpoint and returns the new `runId` and
  `threadId`.

State access complements streaming. Streams provide live observation; state
commands provide explicit reads and time-travel operations.

## Replay and Reconnection

Servers may keep a ring buffer of recent events per thread. Clients use sequence
numbers to recover missed events:

- SSE clients pass `since` in `EventStreamRequest`.
- WebSocket clients call `subscription.reconnect` with `lastEventId` and the
  subscriptions they want restored.

The server replays matching buffered events after the requested point and then
switches to live delivery. If the requested event is no longer buffered, servers
should report that the client missed events so the client can resync through
state commands.

## Extensibility

Most records include an `Extensible` tail, allowing additional text-keyed fields
for forward compatibility. Consumers should ignore unknown fields and default
unknown tagged variants to a safe fallback instead of failing closed.

Content blocks are especially extensible. New block types can be added to
LangChain content block definitions and flow through the same message lifecycle
without changing the transport or channel model.

## Generated Bindings

The `js` and `py` directories contain generated type bindings for the CDDL
schema. They are intended for typing protocol payloads, not as runtime clients.
The packages do not include transport implementations, connection management, or
helper APIs.

When the CDDL schema changes, regenerate the language bindings from
`streaming/protocol.cddl` and keep the generated files in sync.
