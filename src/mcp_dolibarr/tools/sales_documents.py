# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

from datetime import UTC, date, datetime, time
from typing import Literal

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from ..client import Dolibarr
from . import CREATE, ENDPOINTS, IRREVERSIBLE, READ, Limit, Page, SalesDocumentKind, all_of, as_json

# A proposal takes one line on `line`; its `lines` takes a list of lines.
_LINE = {"proposal": "line", "order": "lines", "invoice": "lines"}
_SUMMARY = "id,ref,ref_client,socid,date,fin_validite,date_lim_reglement,total_ht,total_ttc,status"


class Line(BaseModel):
    desc: str = Field(description="Line description")
    qty: float
    subprice: float = Field(description="Unit price excluding tax")
    tva_tx: float = Field(description="VAT rate in percent, e.g. 20")
    fk_product: int | None = Field(None, description="Catalogue product id; empty for a free line")
    product_type: Literal[0, 1] = Field(1, description="0 product, 1 service")
    remise_percent: float | None = Field(None, description="Discount in percent")


def _timestamp(day: date) -> int:
    # Noon UTC falls on the same calendar day in any Dolibarr server time zone.
    return int(datetime.combine(day, time(12), tzinfo=UTC).timestamp())


def register(mcp: FastMCP, api: Dolibarr, allow_write: bool) -> None:
    @mcp.tool(annotations=READ)
    async def list_sales_documents(
        kind: SalesDocumentKind,
        thirdparty_id: int | None = None,
        status: int | None = None,
        sqlfilters: str | None = None,
        limit: Limit = 20,
        page: Page = 0,
    ) -> str:
        """Sales documents (proposals, orders or invoices), newest first.

        The `status` codes are in the instructions.
        """
        status_filter = f"(t.fk_statut:=:{status})" if status is not None else None
        return as_json(
            await api.list(
                ENDPOINTS[kind],
                thirdparty_ids=thirdparty_id,
                sqlfilters=all_of(status_filter, sqlfilters),
                sortfield="t.rowid",
                sortorder="DESC",
                limit=limit,
                page=page,
                properties=_SUMMARY,
            )
        )

    if not allow_write:
        return

    @mcp.tool(annotations=CREATE)
    async def create_sales_document(
        kind: SalesDocumentKind,
        thirdparty_id: int,
        lines: list[Line],
        day: date | None = None,
        ref_client: str | None = None,
        note_public: str | None = None,
    ) -> str:
        """Create a draft proposal, order or invoice with its lines, dated `day` (default today).

        It stays a draft, editable and deletable, until validate_sales_document.
        """
        path = ENDPOINTS[kind]
        date_ = _timestamp(day or date.today())
        new_id = await api.post(
            path,
            {
                "socid": thirdparty_id,
                "date": date_,
                "ref_client": ref_client,
                "note_public": note_public,
            },
        )
        for line in lines:
            await api.post(f"{path}/{new_id}/{_LINE[kind]}", line.model_dump())
        return as_json(await api.get(f"{path}/{new_id}"))

    @mcp.tool(annotations=CREATE)
    async def add_sales_document_line(kind: SalesDocumentKind, id: int, line: Line) -> str:
        """Add a line to a draft proposal, order or invoice; returns the updated document."""
        await api.post(f"{ENDPOINTS[kind]}/{id}/{_LINE[kind]}", line.model_dump())
        return as_json(await api.get(f"{ENDPOINTS[kind]}/{id}"))

    @mcp.tool(annotations=IRREVERSIBLE)
    async def validate_sales_document(kind: SalesDocumentKind, id: int) -> str:
        """Validate a draft: it gets its final reference and can no longer be edited.

        A validated invoice is a legal document: confirm with the user first.
        """
        return as_json(await api.post(f"{ENDPOINTS[kind]}/{id}/validate", {"notrigger": 0}))
