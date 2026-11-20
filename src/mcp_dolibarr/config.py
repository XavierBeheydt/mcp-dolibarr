# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT
# Doc: https://docs.pydantic.dev/latest/concepts/pydantic_settings/

from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

Transport = Literal["stdio", "http"]


class Settings(BaseSettings):
    """Environment, else the `.env` file, else defaults; the command line overrides them."""

    model_config = SettingsConfigDict(env_file=".env")

    dolibarr_url: str
    dolibarr_api_key: SecretStr
    dolibarr_allow_write: bool = False
    mcp_transport: Transport = "stdio"
    mcp_host: str = "127.0.0.1"
    mcp_port: int = 8000
