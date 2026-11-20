# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

import pytest

from mcp_dolibarr.config import Settings


@pytest.fixture(autouse=True)
def env(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)  # no .env here
    monkeypatch.setenv("DOLIBARR_URL", "https://erp.test/api/index.php")
    monkeypatch.setenv("DOLIBARR_API_KEY", "secret")
    monkeypatch.setenv("MCP_PORT", "7000")


def test_defaults_come_after_the_environment() -> None:
    settings = Settings()
    assert settings.mcp_port == 7000
    assert settings.mcp_transport == "stdio"
    assert not settings.dolibarr_allow_write


def test_command_line_beats_the_environment() -> None:
    settings = Settings(
        _cli_parse_args=["--mcp-port", "9000", "--mcp-transport", "http", "--dolibarr-allow-write"]
    )
    assert settings.mcp_port == 9000
    assert settings.mcp_transport == "http"
    assert settings.dolibarr_allow_write


def test_api_key_is_a_secret() -> None:
    assert "secret" not in repr(Settings())
