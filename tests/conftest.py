# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

import json
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import Any

import httpx
import pytest
from mcp import Client

from mcp_dolibarr.client import Dolibarr
from mcp_dolibarr.server import build_server

URL = "https://erp.test/api/index.php"


class MockDolibarr:
    """Answers canned responses by (method, path) and records every request."""

    def __init__(self) -> None:
        self.routes: dict[tuple[str, str], tuple[int, Any]] = {}
        self.requests: list[httpx.Request] = []

    def on(self, method: str, path: str, body: Any, status: int = 200) -> None:
        self.routes[(method, path)] = (status, body)

    def handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        path = request.url.path.removeprefix("/api/index.php/")
        status, body = self.routes.get(
            (request.method, path), (404, {"error": {"code": 404, "message": "Not found"}})
        )
        return httpx.Response(status, json=body)

    def last(self, method: str) -> httpx.Request:
        return [r for r in self.requests if r.method == method][-1]

    def bodies(self, method: str) -> list[Any]:
        return [json.loads(r.content) for r in self.requests if r.method == method]


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def dolibarr() -> MockDolibarr:
    return MockDolibarr()


@pytest.fixture
def api(dolibarr: MockDolibarr) -> Dolibarr:
    return Dolibarr(URL, "test-key", httpx.MockTransport(dolibarr.handle))


@pytest.fixture
def connect(api: Dolibarr) -> Callable[..., AbstractAsyncContextManager[Client]]:
    def _connect(allow_write: bool = False) -> AbstractAsyncContextManager[Client]:
        return Client(build_server(api, allow_write))

    return _connect


async def call(client: Client, tool: str, **arguments: Any) -> Any:
    result = await client.call_tool(tool, arguments)
    assert not result.is_error, result.content[0].text
    return json.loads(result.content[0].text)
