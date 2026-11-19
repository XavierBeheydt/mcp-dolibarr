# Repository layout

Where things live. Read this before creating a file or a directory; if
nothing fits, ask instead of adding a top-level directory.

| Path | Content |
| --- | --- |
| `.agents/` | AI agent instructions (`instructions/`) and skills (`skills/`) |
| `.worktrees/` | Git worktrees, ignored by git (see `repo-workflow.md`) |

Root files: `.editorconfig`, `.gitattributes`, `.gitignore`, `AGENTS.md`,
`README.md`, `LICENSE`.

`.claude/skills` is a symlink to `.agents/skills`, so Claude Code finds the
same skills.

## Rules

- Generated files and caches never go in the tree: they are ignored by git.
- A new directory or a new kind of file updates this page in the same
  change.
