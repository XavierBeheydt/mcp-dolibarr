# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

from importlib.metadata import version

from fastmcp import FastMCP

from .client import Dolibarr
from .tools import products, sales_documents, system, thirdparties

INSTRUCTIONS = """\
Dolibarr ERP/CRM. Objects have a numeric `id` and a business reference `ref`.
Amounts: `total_ht` excludes tax, `total_ttc` includes it. Dates are Unix timestamps.

`sqlfilters` syntax: `(t.column:operator:'value')`, operators = != < > <= >= like in,
combined with `and` / `or`, e.g. `(t.total_ttc:>:1000) and (t.date_lim_reglement:<:'2026-01-01')`.

Status codes (`fk_statut`):
- proposal: 0 draft, 1 validated, 2 signed, 3 not signed, 4 billed
- order: -1 cancelled, 0 draft, 1 validated, 2 in progress, 3 delivered
- invoice: 0 draft, 1 unpaid, 2 paid, 3 abandoned
"""

MODULES = (system, thirdparties, products, sales_documents)

READ_ONLY = "\nThis server is read-only: it cannot change anything in Dolibarr.\n"


def build_server(api: Dolibarr, allow_write: bool) -> FastMCP:
    mcp = FastMCP(
        "dolibarr",
        version=version("mcp-dolibarr"),
        instructions=INSTRUCTIONS + ("" if allow_write else READ_ONLY),
    )
    for module in MODULES:
        module.register(mcp, api, allow_write)
    return mcp
