# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

import json
from typing import Annotated, Any, Literal

from mcp.types import ToolAnnotations
from pydantic import Field

# Hints for the MCP client (it may ask the user before calling a tool). Every tool is closed-world:
# it only talks to the configured Dolibarr. READ never changes anything; IRREVERSIBLE writes at
# once to the live ERP, so the client is told to treat it as destructive.
READ = ToolAnnotations(read_only_hint=True, open_world_hint=False)
CREATE = ToolAnnotations(read_only_hint=False, destructive_hint=False, open_world_hint=False)
IRREVERSIBLE = ToolAnnotations(read_only_hint=False, destructive_hint=True, open_world_hint=False)

ObjectKind = Literal["thirdparty", "contact", "product", "project", "proposal", "order", "invoice"]
SalesDocumentKind = Literal["proposal", "order", "invoice"]

# The API path of each object kind accepted by `get_object`; the model sees only the kind.
ENDPOINTS: dict[str, str] = {
    "thirdparty": "thirdparties",
    "contact": "contacts",
    "product": "products",
    "project": "projects",
    "proposal": "proposals",
    "order": "orders",
    "invoice": "invoices",
}

Limit = Annotated[int, Field(ge=1, le=100)]
Page = Annotated[int, Field(ge=0)]


def like(columns: list[str], text: str) -> str:
    """sqlfilters matching `text` in any of `columns`."""
    # sqlfilters can't escape a quote: the `_` LIKE wildcard stands in for it.
    pattern = text.replace("'", "_")
    return "(" + " or ".join(f"({c}:like:'%{pattern}%')" for c in columns) + ")"


def all_of(*filters: str | None) -> str | None:
    return " and ".join(f for f in filters if f) or None


def as_json(data: Any) -> str:
    """One compact JSON text: lists stay a single readable block, even when empty."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))
