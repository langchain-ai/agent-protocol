# `@langchain/protocol`

TypeScript bindings for the LangChain agent streaming protocol.

This package publishes the generated TypeScript schema bindings from
`protocol.cddl` so TypeScript applications can type protocol commands, events,
results, and content blocks consistently.

## What this package includes

- Generated TypeScript protocol bindings in `protocol.ts`
- Types for top-level messages such as `Command`, `Message`, and protocol events
- Types for protocol modules including session, subscription, resource,
  sandbox, input, state, and usage

## What this package does not include

This package does not currently ship a runtime client, transport, or helper APIs
such as `createSession()`. It is intended for typing protocol payloads and
generated bindings only.

## Installation

```bash
npm install @langchain/protocol
```

## Usage

Use type-only imports when consuming the protocol schema:

```ts
import type {
  Command,
  Message,
  SessionOpenParams,
  SubscribeParams,
  MessagesEvent,
} from "@langchain/protocol";
```

You can then use the exported types to model protocol payloads in your own
transport or client implementation:

```ts
import type { Command, SessionOpenParams } from "@langchain/protocol";

const params: SessionOpenParams = {
  protocolVersion: "0.3.0",
};

const openCommand: Command = {
  id: 1,
  method: "session.open",
  params,
};
```

## Versioning

The package version is aligned with the draft streaming protocol schema version.
The current generated bindings target protocol `0.5.0`.

## Source of truth

The canonical protocol definition lives at `../protocol.cddl`. The TypeScript
bindings in this package are generated from that schema.
