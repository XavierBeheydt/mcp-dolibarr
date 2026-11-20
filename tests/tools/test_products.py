# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

import pytest
from conftest import MockDolibarr, call

pytestmark = pytest.mark.anyio


async def test_search_products_builds_filters(connect, dolibarr: MockDolibarr) -> None:
    dolibarr.on("GET", "products", [{"id": "5", "ref": "SRV-1", "label": "Audit"}])
    async with connect() as client:
        found = await call(client, "search_products", text="Audit", type="service")
    params = dolibarr.last("GET").url.params
    assert found == [{"id": "5", "ref": "SRV-1", "label": "Audit"}]
    assert params["mode"] == "2"
    assert params["sqlfilters"] == "((t.ref:like:'%Audit%') or (t.label:like:'%Audit%'))"
    assert params["sortfield"] == "t.ref"


async def test_empty_search_returns_empty_list(connect) -> None:
    async with connect() as client:
        assert await call(client, "search_products", text="nothing") == []
