# mcp-dolibarr

An [MCP](https://modelcontextprotocol.io) server for the
[Dolibarr](https://www.dolibarr.org) ERP/CRM REST API.

- **Read-only by default.** Write tools only exist when
  `DOLIBARR_ALLOW_WRITE=true`, and carry MCP annotations so the client asks
  before running them.
- **Compact answers.** Empty values are dropped from every answer, to save the
  model's context. The tools are listed in [docs/tools.md](docs/tools.md).

## Dolibarr setup

Dolibarr 24 or later.

1. Enable the **API REST** module (Home → Setup → Modules).
2. Create a dedicated user, give it only the permissions the agent needs
   (read-only rights for a read-only server), and generate its API key on its
   user card.

The API key carries that user's permissions: Dolibarr enforces them whatever
this server allows.

## Configuration

Settings come from the environment; copy `.env.example` to `.env`.

| Variable | Default | Meaning |
| --- | --- | --- |
| `DOLIBARR_URL` | required | API root, ending with `/api/index.php` |
| `DOLIBARR_API_KEY` | required | API key of the Dolibarr user |
| `DOLIBARR_ALLOW_WRITE` | `false` | Register the tools that write to Dolibarr |
| `MCP_TRANSPORT` | `stdio` | `stdio`, or `streamable-http` (served at `/mcp`) |
| `MCP_HOST` | `127.0.0.1` | HTTP bind address |
| `MCP_PORT` | `8000` | HTTP port |

## Run

Requires [uv](https://docs.astral.sh/uv/).

```sh
uv run --env-file .env mcp-dolibarr
```

Claude Code, over stdio:

```sh
claude mcp add dolibarr -- uv run --directory /path/to/mcp-dolibarr --env-file .env mcp-dolibarr
```

The HTTP transport has no authentication: keep it on localhost, or behind a
reverse proxy that authenticates.

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
