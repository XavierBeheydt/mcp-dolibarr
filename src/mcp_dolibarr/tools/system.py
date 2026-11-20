# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

from typing import Any

from fastmcp import FastMCP

from ..client import Dolibarr, Method
from . import ENDPOINTS, IRREVERSIBLE, READ, ObjectKind, as_json


def register(mcp: FastMCP, api: Dolibarr, allow_write: bool) -> None:
    @mcp.tool(annotations=READ)
    async def get_status() -> str:
        """Dolibarr version and API status: checks the connection and the API key."""
        return as_json(await api.get("status"))

    @mcp.tool(annotations=READ)
    async def get_object(kind: ObjectKind, id: int) -> str:
        """Full Dolibarr object by numeric id, with its lines for a proposal, order or invoice."""
        return as_json(await api.get(f"{ENDPOINTS[kind]}/{id}"))

    @mcp.tool(annotations=READ)
    async def dolibarr_get(path: str, params: dict[str, Any] | None = None) -> str:
        """GET a Dolibarr REST endpoint that no other tool covers.

        `path` is relative to the API root, e.g. `projects/3/tasks`, `setup/dictionary/countries`.
        """
        return as_json(await api.request("GET", path, params))

    # Read-only server: stop here. The write tools below are never registered, so the model
    # cannot see them or call them.
    if not allow_write:
        return

    @mcp.tool(annotations=IRREVERSIBLE)
    async def dolibarr_request(
        method: Method,
        path: str,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | list[Any] | None = None,
    ) -> str:
        """Send any request to the Dolibarr REST API, applied at once to the live ERP.

        Use it only when no dedicated tool fits.
        """
        return as_json(await api.request(method, path, params, body))
