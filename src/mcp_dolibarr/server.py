# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

from importlib.metadata import version

from fastmcp import FastMCP

from .client import Dolibarr
from .tools import system, thirdparties

INSTRUCTIONS = """\
Dolibarr ERP/CRM. Objects have a numeric `id` and a business reference `ref`.
Amounts: `total_ht` excludes tax, `total_ttc` includes it. Dates are Unix timestamps.

`sqlfilters` syntax: `(t.column:operator:'value')`, operators = != < > <= >= like in,
combined with `and` / `or`, e.g. `(t.total_ttc:>:1000) and (t.date_lim_reglement:<:'2026-01-01')`.
"""

MODULES = (system, thirdparties)

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
