# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

import pytest
from conftest import MockDolibarr, call

pytestmark = pytest.mark.anyio


async def test_search_thirdparties_builds_filters(connect, dolibarr: MockDolibarr) -> None:
    dolibarr.on("GET", "thirdparties", [{"id": "3", "name": "Mairie d'Annecy"}])
    async with connect() as client:
        found = await call(client, "search_thirdparties", name="d'Annecy", role="customer")
    params = dolibarr.last("GET").url.params
    assert found == [{"id": "3", "name": "Mairie d'Annecy"}]
    assert params["mode"] == "1"
    assert params["sqlfilters"] == "((t.nom:like:'%d_Annecy%') or (t.name_alias:like:'%d_Annecy%'))"


async def test_create_thirdparty_sets_the_role_flags(connect, dolibarr: MockDolibarr) -> None:
    dolibarr.on("POST", "thirdparties", 7)
    dolibarr.on("GET", "thirdparties/7", {"id": "7", "name": "ACME"})
    async with connect(allow_write=True) as client:
        created = await call(client, "create_thirdparty", name="ACME", role="supplier", zip=None)
    assert dolibarr.bodies("POST") == [{"name": "ACME", "fournisseur": 1}]
    assert created == {"id": "7", "name": "ACME"}


async def test_search_without_result_returns_empty_list(connect, dolibarr: MockDolibarr) -> None:
    dolibarr.on(
        "GET", "thirdparties", {"error": {"code": 404, "message": "No suppliers found"}}, 404
    )
    async with connect() as client:
        assert await call(client, "search_thirdparties", name="nobody", role="supplier") == []
