#!/usr/bin/env python3
"""Fixup generated Python protocol bindings.

cddl2py emits definitions in CDDL schema order, which may not satisfy Python's
eager-evaluation constraints.  This script topologically sorts top-level
statements so that every name is defined before its first runtime use.

With ``from __future__ import annotations``, type annotations are lazy strings
and create no runtime dependency.  Only class base classes, class keyword
arguments, and assignment right-hand sides are eagerly evaluated.

It also patches a known cddl2py bug: the string literal ``"text"`` collides
with the CDDL primitive ``text`` and emits as the bare type ``str`` rather
than ``Literal["text"]`` on ``TextContentBlock.type``.

Usage::

    cddl2py protocol.cddl | python3 scripts/fixup.py > out.py
"""
from __future__ import annotations

import ast
import re
import sys


def _names_in(node: ast.AST) -> set[str]:
    """Collect all ``ast.Name.id`` references in *node*'s subtree."""
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


def _runtime_deps(node: ast.stmt) -> set[str]:
    """Return names that must be defined before *node* can execute."""
    deps: set[str] = set()
    if isinstance(node, ast.ClassDef):
        for base in node.bases:
            deps |= _names_in(base)
        for kw in node.keywords:
            deps |= _names_in(kw.value)
    elif isinstance(node, ast.Assign):
        deps |= _names_in(node.value)
    return deps


def _defined_names(node: ast.stmt) -> set[str]:
    """Return the names that *node* introduces into the module scope."""
    if isinstance(node, ast.ClassDef):
        return {node.name}
    if isinstance(node, ast.Assign):
        return {t.id for t in node.targets if isinstance(t, ast.Name)}
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        return {(a.asname or a.name) for a in node.names}
    return set()


_TEXT_TYPE_BUG_RE = re.compile(
    r"(class TextContentBlock\(TypedDict\):\n)    type: str\n",
)


def _patch_text_content_block_type(source: str) -> str:
    """Replace ``type: str`` on ``TextContentBlock`` with ``Literal["text"]``.

    Works around a cddl2py bug where the string literal ``"text"`` is resolved
    as the CDDL primitive ``text`` (i.e. ``str``) instead of a literal.
    """
    new_source, count = _TEXT_TYPE_BUG_RE.subn(
        r'\1    type: Literal["text"]\n', source
    )
    if count != 1:
        msg = (
            "fixup: expected exactly one TextContentBlock.type=str occurrence "
            f"to patch, found {count}. Upstream cddl2py output has changed."
        )
        raise RuntimeError(msg)
    return new_source


def fixup(source: str) -> str:
    source = _patch_text_content_block_type(source)
    tree = ast.parse(source)
    source_lines = source.splitlines(keepends=True)

    if not tree.body:
        return source

    # Collect all names defined in the file (for filtering external deps).
    all_defined: set[str] = set()
    for node in tree.body:
        all_defined |= _defined_names(node)

    # Split AST nodes into blocks, each carrying its source text.
    # A block's text spans from its first line to the line before the next node.
    preamble_end = tree.body[0].lineno - 1  # 0-indexed, exclusive
    preamble = "".join(source_lines[:preamble_end])

    blocks: list[dict] = []
    for i, node in enumerate(tree.body):
        start = node.lineno - 1
        end = (
            tree.body[i + 1].lineno - 1
            if i + 1 < len(tree.body)
            else len(source_lines)
        )
        blocks.append(
            {
                "idx": i,
                "text": "".join(source_lines[start:end]),
                "defined": _defined_names(node),
                "deps": _runtime_deps(node) & all_defined,
                "is_import": isinstance(node, (ast.Import, ast.ImportFrom)),
            }
        )

    # Keep imports at the top in their original order.
    header = [b for b in blocks if b["is_import"]]
    body = [b for b in blocks if not b["is_import"]]

    # Greedy topological sort that preserves original order where possible.
    defined_so_far: set[str] = set()
    for b in header:
        defined_so_far |= b["defined"]

    sorted_body: list[dict] = []
    remaining = list(body)

    while remaining:
        ready = [b for b in remaining if b["deps"] <= defined_so_far]
        if not ready:
            # Cycle or unresolvable — emit the rest in original order.
            sorted_body.extend(sorted(remaining, key=lambda b: b["idx"]))
            break
        pick = min(ready, key=lambda b: b["idx"])
        sorted_body.append(pick)
        defined_so_far |= pick["defined"]
        remaining.remove(pick)

    return (
        preamble
        + "".join(b["text"] for b in header)
        + "".join(b["text"] for b in sorted_body)
    )


if __name__ == "__main__":
    sys.stdout.write(fixup(sys.stdin.read()))
