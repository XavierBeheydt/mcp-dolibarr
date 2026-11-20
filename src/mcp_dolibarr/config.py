# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT
# Doc: https://docs.pydantic.dev/latest/concepts/pydantic_settings/

from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, CliSuppress, SettingsConfigDict


class Settings(BaseSettings):
    """Command-line option, else environment variable, else `.env`, else default."""

    model_config = SettingsConfigDict(env_file=".env", cli_kebab_case=True, cli_implicit_flags=True)

    dolibarr_url: str
    dolibarr_api_key: CliSuppress[SecretStr]
    dolibarr_allow_write: bool = False
    mcp_transport: Literal["stdio", "http"] = "stdio"
    mcp_host: str = "127.0.0.1"
    mcp_port: int = 8000
