# AI Agents Instructions

## The Eleven Commandments

For every agent, on every task:

1. Thou shalt state thy assumptions, and ask when unsure.
2. Thou shalt present every interpretation of a request, and never pick one
   silently.
3. Thou shalt propose the simpler solution when one exists, even against the
   user's idea.
4. Thou shalt stop and ask when something is unclear, saying exactly what.
5. Thou shalt do only what is asked: no hidden feature, no extra option or
   flexibility, except what a `TODO-AI` comment asks (see the
   [todo-ai](.agents/skills/todo-ai/SKILL.md) skill).
6. Thou shalt not handle errors that cannot happen.
7. Thou shalt be concise and compact, in writing and in code, without
   repetition, and rewrite in 50 lines what thou wrote in 200.
8. Thou shalt let the code explain itself, without an avalanche of comments.
9. Thou shalt follow the coding rules strictly. Where none exists, thou shalt
   neither invent one nor mix styles, but ask, and the rule gets added to
   `.agents/`.
10. Thou shalt not touch code next to the change, nor refactor working code,
    unless that is the request.
11. Thou shalt stay agnostic: nothing specific to a person or a machine
    (name, email, path, host) is hardcoded; read it from the configuration.

## Security

Never hardcode a login, password, token, key or any other secret, in code,
configs, docs, commits, PRs or issues. Read it from the environment or a
git-ignored file (e.g. `.env`), and commit only a placeholder file
(`.env.example`). Don't print or repeat a secret in a reply, and don't open
a secret file unless the task needs it. If a secret leaks, stop and tell the
user: it must be rotated, deleting the commit is not enough.

This server drives an ERP holding real invoices and customers:

- Tests never reach a real Dolibarr: they mock it (see `tests/conftest.py`).
- A tool that writes to Dolibarr is registered only when writes are enabled
  (`DOLIBARR_ALLOW_WRITE`), and carries the matching MCP annotations. Never
  add a write path that bypasses this switch.

## Language

English is the language of the repo: code, comments, identifiers, docs,
commits and PRs. Interactive exchanges with the user use the user's language.

## Repository Workflow

Branches (`main`, feature branches), worktrees, commits, pull requests,
releases and tracking: read
[repo-workflow.md](.agents/instructions/repo-workflow.md) before any git,
branch, commit, PR or issue operation.

## Repository Layout

Where files and modules live: read
[.agents/instructions/repo-layout.md](.agents/instructions/repo-layout.md) before
creating a file or a directory.

## Coding Workflow

Every code change follows the same loop; a task is done only when one pass
goes through with everything green:

1. Read the matching [style guide](#style-guide).
2. Code the feature, or the fix (a bug starts with a test that reproduces
   it), following the guide.
3. Format and lint, with the language's [skills](#skills)
   (`<language>-format`, `<language>-lint`).
4. Test, with the language's test skill (`<language>-test`).
5. If any step fails, fix and restart from step 2; otherwise, move on.

If a language has no lint or test skill, say so instead of skipping the step.

For a task of more than one step, state a short plan first, each step with
its check:

1. [Step] → verify: [check]
2. [Step] → verify: [check]

## Style Guide

Language-specific rules live in `.agents/instructions/style/<language>.md`;
read the matching one before editing a file in that language.

Formatting is owned by the language's formatter (ruff for Python).
`.editorconfig` sets indentation and line length only for the file types that
have no formatter (Containerfile, JSON, TOML, YAML, Markdown): add a section
there only for such a type, never for a language that has a formatter.

## Header Comment

Every source or config file starts with a header comment (copyright, license
and, if useful, documentation), in the file's comment syntax and after the
shebang if there is one. Docs and Markdown, generated files and files that
can't hold comments have none.

- A file starts with the organization line and the license identifier
  (the project is under the [MIT License](LICENSE)):
  `Copyright (c) <year> Beheydt.DEV <xavier.beheydt@gmail.com>` then
  `SPDX-License-Identifier: MIT`.
- Then, if useful, a `Doc:` line linking the documentation of the format or
  the tool the file configures.
- `<year>` is the current year.

Example, in a Python file:

```python
# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT
```

## Skills

Procedures live in `.agents/skills/<name>/SKILL.md`; use the matching one
instead of improvising the command:

- [container-build](.agents/skills/container-build/SKILL.md): build and run
  the container image (Podman).
- [dolibarr-api](.agents/skills/dolibarr-api/SKILL.md): check a Dolibarr
  endpoint, or the API changes of a new Dolibarr release.
- [python-deps](.agents/skills/python-deps/SKILL.md): install, add or update
  dependencies (uv).
- [python-format](.agents/skills/python-format/SKILL.md): format with ruff.
- [python-lint](.agents/skills/python-lint/SKILL.md): lint with ruff.
- [python-test](.agents/skills/python-test/SKILL.md): run tests with pytest.
- [todo-ai](.agents/skills/todo-ai/SKILL.md): resolve the `TODO-AI` comments,
  grouped, one subagent per group.
- [vibe](.agents/skills/vibe/SKILL.md): delegate a bounded read-only task to
  Mistral Vibe.

## New language, tool or feature

Introducing a new language adds both a style guide
(`.agents/instructions/style/<language>.md`) and its skills
(`.agents/skills/<language>-format`, `-lint`, `-test`).

Introducing a new tool or feature (CI, runtime, deployment…) adds its skill
(`.agents/skills/<tool>-<action>`) and, if it changes where files live,
updates [repo-layout.md](.agents/instructions/repo-layout.md).

Introducing a new language, file type or tool reviews the repo-wide configs in
the same change, and adapts them only where the default does not fit:
`.editorconfig` (indentation, line length), `.gitattributes` (line endings,
binary files), `.gitignore` (generated outputs and caches), and the formatter
and linter configs of the language.

Each addition is listed in [Skills](#skills) in the same change.

## New MCP tool

A Dolibarr resource gets its tools in `src/mcp_dolibarr/tools/<resource>.py`,
registered from `server.py`; read [docs/tools.md](docs/tools.md) first, and
check the Dolibarr endpoint in the code of the oldest supported version (see
the [dolibarr-api](.agents/skills/dolibarr-api/SKILL.md) skill). Keep
the tool count low: prefer one tool with a `kind` parameter to one tool per
Dolibarr endpoint, and the `dolibarr_get` / `dolibarr_request` passthrough to
a tool used once. A new tool is listed in `docs/tools.md` and tested in
`tests/tools/test_<resource>.py` in the same change.
