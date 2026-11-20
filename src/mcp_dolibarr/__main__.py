# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

from pydantic import ValidationError

from .client import Dolibarr
from .config import Settings
from .server import build_server


def main() -> None:
    try:
        settings = Settings(_cli_parse_args=True)
    except ValidationError as error:
        raise SystemExit(f"Invalid settings, see --help and .env.example:\n{error}") from None
    url = settings.dolibarr_url.rstrip("/")
    api = Dolibarr(url, settings.dolibarr_api_key.get_secret_value())
    server = build_server(api, settings.dolibarr_allow_write)
    if settings.mcp_transport == "stdio":
        server.run(show_banner=False)
    else:
        server.run("http", host=settings.mcp_host, port=settings.mcp_port, show_banner=False)


if __name__ == "__main__":
    main()
