# Repository layout

Where things live. Read this before creating a file or a directory; if
nothing fits, ask instead of adding a top-level directory.

| Path | Content |
| --- | --- |
| `src/mcp_dolibarr/` | The package: `config.py` (settings: command line, environment and `.env`), `client.py` (Dolibarr REST client), `server.py` (MCP server and tool registration), `__main__.py` (entry point) |
| `src/mcp_dolibarr/tools/` | MCP tools, one module per Dolibarr resource, each with a `register()` function |
| `tests/` | pytest tests, one `test_<module>.py` per module; Dolibarr is mocked in `conftest.py` |
| `tests/tools/` | The tests of the MCP tools, one `test_<resource>.py` per `src/mcp_dolibarr/tools/<resource>.py` |
| `docs/` | Documentation (Markdown); no plans or roadmaps, those live in issues |
| `.github/` | GitHub configuration: `workflows/` (CI in `ci.yml`, CodeQL in `codeql.yml`) and `dependabot.yml` |
| `.agents/` | AI agent instructions (`instructions/`) and skills (`skills/`) |
| `.worktrees/` | Git worktrees, ignored by git (see `repo-workflow.md`) |

Root files: `pyproject.toml`, `uv.lock`, `Containerfile`, `.containerignore`,
`.env.example`, `.editorconfig`, `.gitattributes`, `.gitignore`, `AGENTS.md`,
`README.md`, `LICENSE`.

`.claude/skills` is a symlink to `.agents/skills`, so Claude Code finds the
same skills.

## Rules

- Generated files and caches (`.venv/`, `dist/`, `__pycache__/`, tool
  caches) never go in the tree: they are ignored by git.
- A dependency is declared in `pyproject.toml` and pinned by `uv.lock` (see
  the [python-deps](../skills/python-deps/SKILL.md) skill).
- A new directory or a new kind of file updates this page in the same
  change.
