# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

import pytest
from typer.testing import CliRunner

from mcp_dolibarr import __main__ as cli
from mcp_dolibarr.config import Settings

runner = CliRunner()


@pytest.fixture(autouse=True)
def env(monkeypatch: pytest.MonkeyPatch, tmp_path) -> list[Settings]:
    monkeypatch.chdir(tmp_path)  # no .env here
    monkeypatch.setenv("DOLIBARR_URL", "https://erp.test/api/index.php")
    monkeypatch.setenv("DOLIBARR_API_KEY", "secret")
    monkeypatch.setenv("MCP_PORT", "7000")
    served: list[Settings] = []
    monkeypatch.setattr(cli, "serve", served.append)
    return served


def test_environment_beats_defaults(env: list[Settings]) -> None:
    assert runner.invoke(cli.app, []).exit_code == 0
    settings = env[0]
    assert settings.mcp_port == 7000
    assert settings.mcp_transport == "stdio"
    assert not settings.dolibarr_allow_write
    assert "secret" not in repr(settings)


def test_command_line_beats_environment(env: list[Settings]) -> None:
    result = runner.invoke(cli.app, ["--port", "9000", "--transport", "http", "--allow-write"])
    assert result.exit_code == 0
    settings = env[0]
    assert (settings.mcp_port, settings.mcp_transport) == (9000, "http")
    assert settings.dolibarr_allow_write


def test_api_key_is_not_an_option() -> None:
    assert "api-key" not in runner.invoke(cli.app, ["--help"]).output
    assert runner.invoke(cli.app, ["--api-key", "secret"]).exit_code == 2


def test_missing_settings_exit_with_a_message(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DOLIBARR_URL")
    result = runner.invoke(cli.app, [])
    assert result.exit_code == 1
    assert "dolibarr_url" in result.output
