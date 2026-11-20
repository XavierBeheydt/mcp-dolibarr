# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

import pytest
from conftest import MockDolibarr, call

pytestmark = pytest.mark.anyio


async def test_get_object_maps_kind_to_endpoint(connect, dolibarr: MockDolibarr) -> None:
    dolibarr.on("GET", "proposals/4", {"id": "4", "ref": "PR2611-0004", "note": None})
    async with connect() as client:
        assert await call(client, "get_object", kind="proposal", id=4) == {
            "id": "4",
            "ref": "PR2611-0004",
        }


async def test_error_is_reported_to_the_model(connect) -> None:
    async with connect() as client:
        result = await client.call_tool(
            "get_object", {"kind": "invoice", "id": 99}, raise_on_error=False
        )
    assert result.is_error
    assert "Dolibarr 404" in result.content[0].text
