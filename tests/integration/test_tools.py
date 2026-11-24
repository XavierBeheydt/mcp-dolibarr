# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT
"""Every tool against a real, disposable Dolibarr (see the dolibarr-test skill)."""

import os
from collections.abc import AsyncIterator

import pytest
from conftest import call
from fastmcp import Client
from seed import MARKER

from mcp_dolibarr.client import Dolibarr
from mcp_dolibarr.server import build_server

URL = os.environ.get("DOLIBARR_TEST_URL")
KEY = os.environ.get("DOLIBARR_TEST_API_KEY")

pytestmark = [
    pytest.mark.integration,
    pytest.mark.anyio,
    pytest.mark.skipif(not (URL and KEY), reason="DOLIBARR_TEST_URL and _API_KEY unset"),
]

KINDS = ["proposal", "order", "invoice"]
LINE = {"desc": "Integration test line", "qty": 2, "subprice": 50, "tva_tx": 20}


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="module")
async def client() -> AsyncIterator[Client]:
    assert URL and KEY
    async with Client(build_server(Dolibarr(URL, KEY), allow_write=True)) as client:
        found = await call(client, "search_thirdparties", name=MARKER)
        if not found:
            pytest.exit(f"No '{MARKER}' third party at {URL}: not the disposable instance", 2)
        yield client


async def test_get_status(client: Client) -> None:
    status = await call(client, "get_status")
    expected = os.environ.get("DOLIBARR_VERSION")
    assert status["success"]["dolibarr_version"] == expected or not expected


@pytest.mark.parametrize(
    ("kind", "path"),
    [
        ("thirdparty", "thirdparties"),
        ("contact", "contacts"),
        ("product", "products"),
        ("project", "projects"),
        ("proposal", "proposals"),
        ("order", "orders"),
        ("invoice", "invoices"),
    ],
)
async def test_get_object(client: Client, kind: str, path: str) -> None:
    [first] = await call(client, "dolibarr_get", path=path, params={"limit": 1})
    found = await call(client, "get_object", kind=kind, id=int(first["id"]))
    assert found["id"] == first["id"]


async def test_search_thirdparties_with_an_apostrophe(client: Client) -> None:
    found = await call(client, "search_thirdparties", name="L'Atelier d'Annecy")
    assert [t["name"] for t in found] == ["L'Atelier d'Annecy"]


@pytest.mark.parametrize(
    ("role", "name"), [("supplier", "Supplier Only Ltd"), ("prospect", "Prospect Corp")]
)
async def test_search_thirdparties_by_role(client: Client, role: str, name: str) -> None:
    names = {t["name"] for t in await call(client, "search_thirdparties", role=role, limit=100)}
    customers = {t["name"] for t in await call(client, "search_thirdparties", role="customer")}
    assert name in names
    assert name not in customers


async def test_search_thirdparties_without_result(client: Client) -> None:
    assert await call(client, "search_thirdparties", name="no such company") == []
    assert await call(client, "search_thirdparties", name="no such", role="supplier") == []


async def test_search_products(client: Client) -> None:
    services = await call(client, "search_products", type="service", limit=100)
    [first] = await call(client, "search_products", text=services[0]["ref"], limit=1)
    assert services
    assert {p["type"] for p in services} == {"1"}
    assert first["ref"] == services[0]["ref"]
    assert await call(client, "search_products", text="no such product") == []


@pytest.mark.parametrize("kind", KINDS)
async def test_list_sales_documents(client: Client, kind: str) -> None:
    documents = await call(client, "list_sales_documents", kind=kind, limit=50)
    first = documents[0]
    by_status = await call(client, "list_sales_documents", kind=kind, status=int(first["status"]))
    of_thirdparty = await call(
        client, "list_sales_documents", kind=kind, thirdparty_id=int(first["socid"])
    )
    ids = [int(d["id"]) for d in documents]
    assert ids == sorted(ids, reverse=True)
    assert {str(d["status"]) for d in by_status} == {str(first["status"])}
    assert {d["socid"] for d in of_thirdparty} == {first["socid"]}


async def test_dolibarr_get(client: Client) -> None:
    countries = await call(
        client, "dolibarr_get", path="setup/dictionary/countries", params={"limit": 5}
    )
    assert len(countries) == 5


async def test_create_thirdparty(client: Client) -> None:
    created = await call(
        client, "create_thirdparty", name="Integration Customer", role="customer", town="Annecy"
    )
    assert (created["name"], created["client"], created["town"]) == (
        "Integration Customer",
        "1",
        "Annecy",
    )


@pytest.mark.parametrize("kind", KINDS)
async def test_create_complete_and_validate_a_sales_document(client: Client, kind: str) -> None:
    [customer] = await call(client, "search_thirdparties", name="L'Atelier d'Annecy")
    draft = await call(
        client,
        "create_sales_document",
        kind=kind,
        thirdparty_id=int(customer["id"]),
        lines=[LINE],
        day="2026-01-15",
        ref_client="IT-1",
    )
    updated = await call(
        client, "add_sales_document_line", kind=kind, id=int(draft["id"]), line=LINE
    )
    await call(client, "validate_sales_document", kind=kind, id=int(draft["id"]))
    validated = await call(client, "get_object", kind=kind, id=int(draft["id"]))
    assert draft["ref"].startswith("(PROV")
    assert len(updated["lines"]) == 2
    assert float(updated["total_ht"]) == 200
    assert not validated["ref"].startswith("(PROV")
    assert int(validated["status"]) == 1


async def test_dolibarr_request_deletes_a_draft(client: Client) -> None:
    [customer] = await call(client, "search_thirdparties", name="L'Atelier d'Annecy")
    draft = await call(
        client,
        "create_sales_document",
        kind="proposal",
        thirdparty_id=int(customer["id"]),
        lines=[],
    )
    await call(client, "dolibarr_request", method="DELETE", path=f"proposals/{draft['id']}")
    result = await client.call_tool(
        "get_object", {"kind": "proposal", "id": int(draft["id"])}, raise_on_error=False
    )
    assert result.is_error
    assert "404" in result.content[0].text
