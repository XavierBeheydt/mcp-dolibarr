# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

import pytest
from typer.testing import CliRunner

from mcp_dolibarr import __main__ as cli
from mcp_dolibarr.__main__ import serve
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


def test_path_comes_from_the_environment_or_the_command_line(
    monkeypatch: pytest.MonkeyPatch, env: list[Settings]
) -> None:
    assert runner.invoke(cli.app, []).exit_code == 0
    assert env[0].mcp_path == "/mcp"
    monkeypatch.setenv("MCP_PATH", "/from-env")
    assert runner.invoke(cli.app, []).exit_code == 0
    assert runner.invoke(cli.app, ["--path", "/from-cli"]).exit_code == 0
    assert [settings.mcp_path for settings in env[1:]] == ["/from-env", "/from-cli"]


def test_path_must_start_with_a_slash() -> None:
    result = runner.invoke(cli.app, ["--path", "dolibarr"])
    assert result.exit_code == 1
    assert "mcp_path" in result.output


def test_http_server_runs_on_the_path(monkeypatch: pytest.MonkeyPatch) -> None:
    runs: list[tuple] = []

    class Server:
        def run(self, *args, **kwargs) -> None:
            runs.append((args, kwargs))

    monkeypatch.setattr(cli, "build_server", lambda api, allow_write: Server())
    serve(
        Settings(
            dolibarr_url="https://erp.test",
            dolibarr_api_key="k",
            mcp_transport="http",
            mcp_path="/dolibarr",
        )
    )
    assert runs == [
        (("http",), {"host": "127.0.0.1", "port": 7000, "path": "/dolibarr", "show_banner": False})
    ]
