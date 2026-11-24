---
name: github-release
description: Release a new version (tag, container image, PyPI package, GitHub release). Use when asked to release, tag or publish a version, or when the Release workflow fails.
---

# GitHub release

Never tag unless the user asks. The steps, from
[repo-workflow.md](../../instructions/repo-workflow.md#releases):

1. A `chore(release): vX.Y.Z` PR into `dev` sets `version` in
   `pyproject.toml` (`uv version X.Y.Z`, which updates `uv.lock` too), in
   the PEP 440 spelling for a pre-release (`X.Y.ZaN`, `X.Y.ZbN`, `X.Y.ZrcN`).
2. A `dev` → `main` PR, merged with a merge commit.
3. Once CI is green on `main`, tag the merge commit and push the tag:

   ```sh
   git fetch origin main
   git tag -a vX.Y.Z -m vX.Y.Z origin/main
   git push origin vX.Y.Z
   ```

The tag starts `.github/workflows/release.yml`:

- `check`: the tag must be `vX.Y.Z` or `vX.Y.Z-(alpha|beta|rc).N` and match
  `pyproject.toml`; nothing is published otherwise.
- `image`: the `linux/amd64` and `linux/arm64` image on
  `ghcr.io/<owner>/mcp-dolibarr`, tagged `X.Y.Z`, `X.Y` and `latest` (only
  `X.Y.Z-…` for a pre-release). Every push to `dev` also publishes `dev`.
- `pypi`: the package on PyPI, or TestPyPI for a pre-release, by trusted
  publishing (no token), from the `pypi` or `testpypi` environment.
- `github-release`: the GitHub release with the package files and generated
  notes, marked pre-release for a pre-release.

A version published on PyPI can never be uploaded again: if `pypi` fails
after the upload, fix forward with a new patch version, never by moving the
tag.

## Maintainer setup (once)

- A trusted publisher on pypi.org and on test.pypi.org: this repository,
  workflow `release.yml`, environment `pypi` (resp. `testpypi`).
- The `pypi` and `testpypi` environments in the repository settings.
- Make the `ghcr.io` package public after its first push.
