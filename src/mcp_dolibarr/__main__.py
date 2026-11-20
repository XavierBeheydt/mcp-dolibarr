# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT

from .client import Dolibarr
from .config import Settings
from .server import build_server


def main() -> None:
    settings = Settings.from_env()
    api = Dolibarr(settings.dolibarr_url, settings.dolibarr_api_key)
    server = build_server(api, settings.allow_write)
    if settings.transport == "stdio":
        server.run()
    else:
        server.run("http", host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
