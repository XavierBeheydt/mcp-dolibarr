---
name: python-typecheck
description: Type-check Python code with mypy. Use before committing Python changes or when configuring mypy.
---

# Python type check

Run `uv run mypy` from the project root. It checks `src/` in strict mode, as
set in `[tool.mypy]` (`pyproject.toml`); don't pass flags or override it.
Tests are out of scope.
