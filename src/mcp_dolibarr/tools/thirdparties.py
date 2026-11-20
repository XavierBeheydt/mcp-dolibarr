# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

from typing import Any, Literal

from fastmcp import FastMCP

from ..client import Dolibarr
from . import CREATE, READ, Limit, Page, as_json, like

Role = Literal["customer", "prospect", "supplier"]

_MODES = {"customer": 1, "prospect": 2, "supplier": 4}
_ROLE_FIELDS = {
    "customer": {"client": 1},
    "prospect": {"client": 2},
    "supplier": {"fournisseur": 1},
}
_SUMMARY = "id,name,name_alias,code_client,code_fournisseur,email,phone,town,client,fournisseur"


def register(mcp: FastMCP, api: Dolibarr, allow_write: bool) -> None:
    @mcp.tool(annotations=READ)
    async def search_thirdparties(
        name: str | None = None, role: Role | None = None, limit: Limit = 20, page: Page = 0
    ) -> str:
        """Third parties (companies or people) whose name or alias contains `name`."""
        return as_json(
            await api.list(
                "thirdparties",
                mode=_MODES[role] if role else None,
                sqlfilters=like(["t.nom", "t.name_alias"], name) if name else None,
                sortfield="t.nom",
                sortorder="ASC",
                limit=limit,
                page=page,
                properties=_SUMMARY,
            )
        )

    if not allow_write:
        return

    @mcp.tool(annotations=CREATE)
    async def create_thirdparty(
        name: str,
        role: Role,
        email: str | None = None,
        phone: str | None = None,
        address: str | None = None,
        zip: str | None = None,
        town: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> str:
        """Create a third party; `extra` takes any other Dolibarr thirdparty field."""
        fields = dict(name=name, email=email, phone=phone, address=address, zip=zip, town=town)
        new_id = await api.post("thirdparties", fields | _ROLE_FIELDS[role] | (extra or {}))
        return as_json(await api.get(f"thirdparties/{new_id}"))
