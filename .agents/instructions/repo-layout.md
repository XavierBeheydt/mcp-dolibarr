# Repository layout

Where things live. Read this before creating a file or a directory; if
nothing fits, ask instead of adding a top-level directory.

| Path | Content |
| --- | --- |
| `src/mcp_dolibarr/` | The package: `client.py` (Dolibarr REST client) |
| `tests/` | pytest tests, one `test_<module>.py` per module; Dolibarr is mocked in `conftest.py` |
| `.agents/` | AI agent instructions (`instructions/`) and skills (`skills/`) |
| `.worktrees/` | Git worktrees, ignored by git (see `repo-workflow.md`) |

Root files: `pyproject.toml`, `uv.lock`, `.editorconfig`, `.gitattributes`,
`.gitignore`, `AGENTS.md`, `README.md`, `LICENSE`.

`.claude/skills` is a symlink to `.agents/skills`, so Claude Code finds the
same skills.

## Rules

- Generated files and caches (`.venv/`, `dist/`, `__pycache__/`, tool
  caches) never go in the tree: they are ignored by git.
- A dependency is declared in `pyproject.toml` and pinned by `uv.lock` (see
  the [python-deps](../skills/python-deps/SKILL.md) skill).
- A new directory or a new kind of file updates this page in the same
  change.
