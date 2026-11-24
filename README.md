# mcp-dolibarr

An [MCP](https://modelcontextprotocol.io) server for the
[Dolibarr](https://www.dolibarr.org) ERP/CRM REST API: lets Claude, or any MCP
client, search third parties and products, read proposals, orders and
invoices, and, when enabled, draft and validate them.

- **Read-only by default.** Write tools only exist when
  `DOLIBARR_ALLOW_WRITE=true`, and carry MCP annotations so the client asks
  before running them.
- **Few tools.** 11 at most ([docs/tools.md](docs/tools.md)), with a `kind`
  parameter for proposals, orders and invoices, and a raw passthrough for the
  rest of the API.
- **Compact answers.** Lists ask Dolibarr only for summary fields, and empty
  values are dropped from every answer, to save the model's context.

## Dolibarr setup

Dolibarr 24 or later.

1. Enable the **API REST** module (Home → Setup → Modules).
2. Create a dedicated user, give it only the permissions the agent needs
   (read-only rights for a read-only server), and generate its API key on its
   user card.

The API key carries that user's permissions: Dolibarr enforces them whatever
this server allows.

## Configuration

Each setting is an environment variable and, except the API key, a command-line
option (`--url`, `--port`... see `mcp-dolibarr --help`). The option
wins over the variable, which wins over the `.env` file of the working directory
(copy `.env.example`), which wins over the default. Keep the API key in the
environment or in `.env`: an option would show in `ps` and in the shell history.

| Variable | Default | Meaning |
| --- | --- | --- |
| `DOLIBARR_URL` | required | API root, ending with `/api/index.php` |
| `DOLIBARR_API_KEY` | required | API key of the Dolibarr user |
| `DOLIBARR_ALLOW_WRITE` | `false` | Register the tools that write to Dolibarr |
| `MCP_TRANSPORT` | `stdio` | `stdio`, or `http` (streamable HTTP) |
| `MCP_HOST` | `127.0.0.1` | HTTP bind address |
| `MCP_PORT` | `8000` | HTTP port |
| `MCP_PATH` | `/mcp` | HTTP path, starting with `/` |

## Run

Requires [uv](https://docs.astral.sh/uv/).

```sh
uv run mcp-dolibarr
```

Claude Code, over stdio:

```sh
claude mcp add dolibarr -- uv run --directory /path/to/mcp-dolibarr mcp-dolibarr
```

Container, over HTTP (see the
[container-build](.agents/skills/container-build/SKILL.md) skill):

```sh
podman build -t mcp-dolibarr -f Containerfile .
podman run --rm --env-file .env -p 127.0.0.1:8000:8000 mcp-dolibarr
```

The HTTP transport has no authentication: keep it on localhost, or behind a
reverse proxy that authenticates (see
[Deployment](docs/deployment.md), with a Traefik example).

## Contributing

Issues and pull requests are welcome.

- One issue per change. Branch from `dev`, named `<type>/<short-description>`
  (`feat/`, `fix/`, `docs/`…).
- Commits and pull request titles follow
  [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
- Pull requests target `dev` and are squash-merged; `dev` goes to `main` at
  each release.

AI coding agents follow [AGENTS.md](AGENTS.md).

### Development

With [uv](https://docs.astral.sh/uv/):

```sh
uv sync --extra dev
uv run ruff format && uv run ruff check && uv run pytest -q
```

## License

[MIT](LICENSE)
