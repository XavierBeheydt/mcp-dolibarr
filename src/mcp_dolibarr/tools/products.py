# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

from typing import Literal

from fastmcp import FastMCP

from ..client import Dolibarr
from . import READ, Limit, Page, as_json, like

_MODES = {"product": 1, "service": 2}
_SUMMARY = "id,ref,label,type,price,price_ttc,tva_tx,status,status_buy,stock_reel"


def register(mcp: FastMCP, api: Dolibarr, allow_write: bool) -> None:
    @mcp.tool(annotations=READ)
    async def search_products(
        text: str | None = None,
        type: Literal["product", "service"] | None = None,
        limit: Limit = 20,
        page: Page = 0,
    ) -> str:
        """Products and services whose reference or label contains `text`."""
        return as_json(
            await api.list(
                "products",
                mode=_MODES[type] if type else None,
                sqlfilters=like(["t.ref", "t.label"], text) if text else None,
                sortfield="t.ref",
                sortorder="ASC",
                limit=limit,
                page=page,
                properties=_SUMMARY,
            )
        )
