# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

from importlib.metadata import version

import pytest

pytestmark = pytest.mark.anyio

READ_TOOLS = {
    "get_status",
    "get_object",
    "dolibarr_get",
    "search_thirdparties",
    "search_products",
    "list_sales_documents",
}
WRITE_TOOLS = {
    "dolibarr_request",
    "create_thirdparty",
    "create_sales_document",
    "add_sales_document_line",
    "validate_sales_document",
}


async def test_read_only_server_has_only_read_tools(connect) -> None:
    async with connect() as client:
        tools = await client.list_tools()
        assert {t.name for t in tools} == READ_TOOLS
        assert all(t.annotations.read_only_hint for t in tools)
        assert "read-only" in client.instructions


async def test_write_tools_are_annotated(connect) -> None:
    async with connect(allow_write=True) as client:
        tools = {t.name: t.annotations for t in await client.list_tools()}
        assert set(tools) == READ_TOOLS | WRITE_TOOLS
        assert not any(tools[name].read_only_hint for name in WRITE_TOOLS)
        assert tools["validate_sales_document"].destructive_hint
        assert tools["dolibarr_request"].destructive_hint
        assert "read-only" not in client.instructions


async def test_server_announces_its_own_version(connect) -> None:
    async with connect() as client:
        assert client.server_info.version == version("mcp-dolibarr")
