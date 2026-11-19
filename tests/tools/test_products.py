# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

import pytest
from conftest import call

pytestmark = pytest.mark.anyio


async def test_empty_search_returns_empty_list(connect) -> None:
    async with connect() as client:
        assert await call(client, "search_products", text="nothing") == []
