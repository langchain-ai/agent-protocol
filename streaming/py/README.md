# langchain-protocol

Python bindings for the [LangChain agent streaming protocol][streaming].

This package provides generated `TypedDict` and `Literal` definitions for the
protocol's commands, events, results, and payload shapes. It does not include a
runtime client, transport, or helper APIs &mdash; it is intended as a source of
typing primitives only.

The types are generated from [`protocol.cddl`][cddl], the source of truth for
the wire format. See the [streaming protocol overview][streaming] for the
full design, channel model, and transport details.

[streaming]: https://github.com/langchain-ai/agent-protocol/tree/main/streaming
[cddl]: https://github.com/langchain-ai/agent-protocol/blob/main/streaming/protocol.cddl

## Installation

```bash
pip install langchain-protocol
```

## Usage

```python
from langchain_protocol import Command, SubscribeParams

params: SubscribeParams = {
    "channels": ["messages", "lifecycle"],
}

subscribe: Command = {
    "id": 1,
    "method": "subscription.subscribe",
    "params": params,
}
```

## What this package includes

- `TypedDict` definitions for commands, events, results, and payload shapes
- `Literal` and union aliases for protocol enums and tagged unions
- A `py.typed` marker so type checkers pick up the bundled annotations
