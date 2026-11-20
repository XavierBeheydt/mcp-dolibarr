# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

import json
from typing import Any, Literal

from mcp.types import ToolAnnotations

# Hints for the MCP client (it may ask the user before calling a tool). Every tool is closed-world:
# it only talks to the configured Dolibarr. READ never changes anything; IRREVERSIBLE writes at
# once to the live ERP, so the client is told to treat it as destructive.
READ = ToolAnnotations(read_only_hint=True, open_world_hint=False)
IRREVERSIBLE = ToolAnnotations(read_only_hint=False, destructive_hint=True, open_world_hint=False)

ObjectKind = Literal["thirdparty", "contact", "product", "project", "proposal", "order", "invoice"]

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


def as_json(data: Any) -> str:
    """One compact JSON text: lists stay a single readable block, even when empty."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))
