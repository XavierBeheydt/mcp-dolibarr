# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

import pytest
from conftest import MockDolibarr

from mcp_dolibarr.client import Dolibarr, DolibarrError, compact

pytestmark = pytest.mark.anyio


def test_compact_drops_empty_values_but_keeps_zero() -> None:
    data = {"a": None, "b": "", "c": [], "d": {"e": None}, "f": 0, "g": [{"h": "", "i": 1}]}
    assert compact(data) == {"f": 0, "g": [{"i": 1}]}


async def test_sends_the_api_key(api: Dolibarr, dolibarr: MockDolibarr) -> None:
    dolibarr.on("GET", "status", {"success": {"code": 200}})
    await api.get("status")
    assert dolibarr.last("GET").headers["DOLAPIKEY"] == "test-key"


async def test_get_drops_none_params(api: Dolibarr, dolibarr: MockDolibarr) -> None:
    dolibarr.on("GET", "products", [])
    await api.get("products", limit=5, mode=None)
    assert dict(dolibarr.last("GET").url.params) == {"limit": "5"}


async def test_list_turns_404_into_empty_list(api: Dolibarr) -> None:
    assert await api.list("invoices") == []


async def test_get_keeps_404_as_error(api: Dolibarr) -> None:
    with pytest.raises(DolibarrError, match="Dolibarr 404"):
        await api.get("invoices/99")


async def test_error_carries_dolibarr_message_and_hint(
    api: Dolibarr, dolibarr: MockDolibarr
) -> None:
    dolibarr.on("GET", "invoices/1", {"error": {"code": 403, "message": "Access denied"}}, 403)
    with pytest.raises(DolibarrError, match=r"403 \(the API user lacks the permission\): Access"):
        await api.get("invoices/1")


async def test_post_drops_none_fields(api: Dolibarr, dolibarr: MockDolibarr) -> None:
    dolibarr.on("POST", "thirdparties", 7)
    assert await api.post("thirdparties", {"name": "ACME", "email": None}) == 7
    assert dolibarr.bodies("POST") == [{"name": "ACME"}]
