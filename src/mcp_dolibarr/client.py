# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

from typing import Any, Literal

import httpx
from mcp.server.mcpserver.exceptions import ToolError

Method = Literal["GET", "POST", "PUT", "DELETE"]

_HINTS = {
    401: "invalid API key",
    403: "the API user lacks the permission",
    404: "not found, or the module is disabled in Dolibarr",
    500: "Dolibarr internal error, see its logs",
}


def compact(data: Any) -> Any:
    """Drop the null and empty values that fill Dolibarr objects, to save the model's context."""
    if isinstance(data, dict):
        items = ((k, compact(v)) for k, v in data.items())
        return {k: v for k, v in items if v not in (None, "", [], {})}
    if isinstance(data, list):
        return [compact(v) for v in data]
    return data


def _error_message(response: httpx.Response) -> str:
    try:
        error = response.json()["error"]
        return error["message"] if isinstance(error, dict) else str(error)
    except (ValueError, KeyError, TypeError):
        return response.text[:500]


class DolibarrError(ToolError):
    """A Dolibarr HTTP error, shown to the model with Dolibarr's own message and a hint."""

    def __init__(self, status: int, message: str) -> None:
        hint = f" ({_HINTS[status]})" if status in _HINTS else ""
        super().__init__(f"Dolibarr {status}{hint}: {message}")
        self.status = status


class Dolibarr:
    def __init__(
        self, url: str, api_key: str, transport: httpx.AsyncBaseTransport | None = None
    ) -> None:
        self._http = httpx.AsyncClient(
            base_url=url,
            headers={"DOLAPIKEY": api_key, "Accept": "application/json"},
            timeout=30,
            transport=transport,
        )

    async def request(
        self, method: Method, path: str, params: dict[str, Any] | None = None, body: Any = None
    ) -> Any:
        """Send a request; return the answer without its empty values, or raise DolibarrError."""
        params = {k: v for k, v in (params or {}).items() if v is not None}
        response = await self._http.request(
            method, "/" + path.lstrip("/"), params=params, json=body
        )
        if response.is_error:
            raise DolibarrError(response.status_code, _error_message(response))
        return compact(response.json())

    async def get(self, path: str, **params: Any) -> Any:
        return await self.request("GET", path, params)

    async def list(self, path: str, **params: Any) -> list[Any]:
        """GET a list: Dolibarr answers an empty one with a 404, returned here as `[]`.

        A 404 on a single object stays an error: use `get` for those.
        """
        try:
            return await self.get(path, **params)
        except DolibarrError as error:
            if error.status == 404:
                return []
            raise

    async def post(self, path: str, body: dict[str, Any]) -> Any:
        return await self.request(
            "POST", path, body={k: v for k, v in body.items() if v is not None}
        )
