# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT
# Doc: https://typer.tiangolo.com/

from typing import Annotated

import typer
from pydantic import ValidationError

from .client import Dolibarr
from .config import Settings, Transport
from .server import build_server

app = typer.Typer(add_completion=False, pretty_exceptions_enable=False)


def serve(settings: Settings) -> None:
    api = Dolibarr(settings.dolibarr_url.rstrip("/"), settings.dolibarr_api_key.get_secret_value())
    server = build_server(api, settings.dolibarr_allow_write)
    if settings.mcp_transport == "stdio":
        server.run(show_banner=False)
    else:
        server.run(
            "http",
            host=settings.mcp_host,
            port=settings.mcp_port,
            path=settings.mcp_path,
            show_banner=False,
        )


@app.command(
    help="MCP server for the Dolibarr REST API. The API key is read from DOLIBARR_API_KEY."
)
def main(
    url: Annotated[str | None, typer.Option(help="Dolibarr API root (env: DOLIBARR_URL)")] = None,
    allow_write: Annotated[
        bool | None,
        typer.Option(
            "--allow-write/--read-only",
            help="Register the tools that write to Dolibarr (env: DOLIBARR_ALLOW_WRITE)",
        ),
    ] = None,
    transport: Annotated[
        Transport | None, typer.Option(help="stdio, or http (env: MCP_TRANSPORT)")
    ] = None,
    host: Annotated[str | None, typer.Option(help="HTTP bind address (env: MCP_HOST)")] = None,
    port: Annotated[int | None, typer.Option(help="HTTP port (env: MCP_PORT)")] = None,
    path: Annotated[
        str | None, typer.Option(help="HTTP path, default /mcp (env: MCP_PATH)")
    ] = None,
) -> None:
    options = {
        "dolibarr_url": url,
        "dolibarr_allow_write": allow_write,
        "mcp_transport": transport,
        "mcp_host": host,
        "mcp_port": port,
        "mcp_path": path,
    }
    try:
        settings = Settings(**{name: value for name, value in options.items() if value is not None})
    except ValidationError as error:
        raise SystemExit(f"Invalid settings, see --help and .env.example:\n{error}") from None
    serve(settings)


if __name__ == "__main__":
    app()
