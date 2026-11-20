---
name: python-deps
description: Install, add or update Python dependencies and environments with uv. Use when syncing the environment, adding a package or touching uv.lock.
---

# Python dependencies

- `uv sync` creates or updates the environment from `pyproject.toml`.
- `uv add <package>` adds a runtime dependency; `uv add --optional dev <package>`
  adds a dev one.
- Commit `uv.lock` with every dependency change.

## Major versions

The dependencies whose API our code is written against (`fastmcp`, `mcp`) are
capped at the next major (`fastmcp>=4.2.2,<5`). A new major above a cap, seen by
Dependabot or by `uv lock --upgrade`, is never taken silently:

1. Do not raise the cap on your own: tell the user, with the upstream
   migration guide and what breaks for us.
2. If the user agrees, raise it in a dedicated `build(deps)` change, together
   with the code migration and the tests, never mixed with other updates.
3. A Dependabot pull request that raises a cap follows the same steps.
