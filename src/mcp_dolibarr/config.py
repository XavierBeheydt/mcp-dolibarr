# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

import os
from dataclasses import dataclass
from typing import Literal

Transport = Literal["stdio", "http"]


@dataclass(frozen=True)
class Settings:
    dolibarr_url: str
    dolibarr_api_key: str
    allow_write: bool = False
    transport: Transport = "stdio"
    host: str = "127.0.0.1"
    port: int = 8000

    @classmethod
    def from_env(cls) -> "Settings":
        transport = os.environ.get("MCP_TRANSPORT", "stdio")
        if transport not in ("stdio", "http"):
            raise SystemExit(f"MCP_TRANSPORT must be stdio or http, not {transport!r}")
        try:
            return cls(
                dolibarr_url=os.environ["DOLIBARR_URL"].rstrip("/"),
                dolibarr_api_key=os.environ["DOLIBARR_API_KEY"],
                allow_write=os.environ.get("DOLIBARR_ALLOW_WRITE", "").lower() in ("1", "true"),
                transport=transport,
                host=os.environ.get("MCP_HOST", "127.0.0.1"),
                port=int(os.environ.get("MCP_PORT", "8000")),
            )
        except KeyError as missing:
            raise SystemExit(f"Missing environment variable {missing}, see .env.example") from None
