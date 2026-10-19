# Protocol generation tooling

Install the locked tool dependencies with `uv sync --frozen --no-install-project`.
The tooling itself is a placeholder package; server generation uses the
`fastapi-codegen` entry point and the flags in `Makefile`.

## Generator security override

`datamodel-code-generator` is pinned to 0.81.0 through a tooling-local uv override
to fix [CVE-2026-107377](https://nvd.nist.gov/vuln/detail/CVE-2026-107377).
`fastapi-code-generator` 0.8.1 still declares `<0.66`; no newer parent release is
available. The override retains the existing generator, HTTP extra, and command
line rather than replacing the generation pipeline.

Before the override, all nine output files from the current `openapi.json` were
captured using fastapi-code-generator 0.8.1 and datamodel-code-generator 0.65.1.
The fixed combination produces byte-identical output, including models and all
six router modules. The compatibility test checks these baseline digests:

```sh
uv run --frozen --no-sync python -m unittest discover -s tests
```

Run it after changing either generator. Intentional specification or generation
changes require reviewing and updating the baseline digests. Remove the override
when the parent supports a fixed generator natively.
