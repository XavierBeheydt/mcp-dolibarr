# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

from datetime import UTC, datetime

import pytest
from conftest import MockDolibarr, call

pytestmark = pytest.mark.anyio


async def test_list_sales_documents_combines_status_and_filters(
    connect, dolibarr: MockDolibarr
) -> None:
    dolibarr.on("GET", "invoices", [])
    async with connect() as client:
        await call(
            client,
            "list_sales_documents",
            kind="invoice",
            status=1,
            sqlfilters="(t.total_ttc:>:100)",
        )
    params = dolibarr.last("GET").url.params
    assert params["sqlfilters"] == "(t.fk_statut:=:1) and (t.total_ttc:>:100)"


async def test_create_sales_document_posts_header_then_lines(
    connect, dolibarr: MockDolibarr
) -> None:
    dolibarr.on("POST", "invoices", 12)
    dolibarr.on("POST", "invoices/12/lines", 1)
    dolibarr.on("GET", "invoices/12", {"id": "12", "ref": "(PROV12)"})
    line = {"desc": "Audit", "qty": 2, "subprice": 500, "tva_tx": 20}
    async with connect(allow_write=True) as client:
        doc = await call(
            client,
            "create_sales_document",
            kind="invoice",
            thirdparty_id=3,
            lines=[line],
            day="2026-11-19",
        )
    header, sent_line = dolibarr.bodies("POST")
    assert doc["ref"] == "(PROV12)"
    assert header == {"socid": 3, "date": int(datetime(2026, 11, 19, 12, tzinfo=UTC).timestamp())}
    assert sent_line == line | {"product_type": 1}


async def test_add_sales_document_line_returns_the_updated_document(
    connect, dolibarr: MockDolibarr
) -> None:
    dolibarr.on("POST", "orders/5/lines", 2)
    dolibarr.on("GET", "orders/5", {"id": "5", "lines": [{"desc": "Support"}]})
    line = {"desc": "Support", "qty": 1, "subprice": 90, "tva_tx": 20, "fk_product": 8}
    async with connect(allow_write=True) as client:
        doc = await call(client, "add_sales_document_line", kind="order", id=5, line=line)
    assert dolibarr.bodies("POST") == [line | {"product_type": 1}]
    assert doc == {"id": "5", "lines": [{"desc": "Support"}]}


async def test_validate_sales_document(connect, dolibarr: MockDolibarr) -> None:
    dolibarr.on("POST", "proposals/4/validate", {"id": "4", "ref": "PR2611-0004"})
    async with connect(allow_write=True) as client:
        await call(client, "validate_sales_document", kind="proposal", id=4)
    assert dolibarr.bodies("POST") == [{"notrigger": 0}]
