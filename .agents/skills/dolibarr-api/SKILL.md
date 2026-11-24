---
name: dolibarr-api
description: Check a Dolibarr REST endpoint against the upstream code, or review the API changes of a new Dolibarr release. Use before adding or changing an MCP tool, or to handle a "Dolibarr API changes" issue.
---

# Dolibarr API

The supported versions and the source file of each endpoint are in the
"Dolibarr API reference" section of `docs/tools.md`.

## Read an endpoint

Every REST module is a class `htdocs/<module>/class/api_<resource>.class.php`;
the table in `docs/tools.md` maps each endpoint to its file. Thirdparties
(`societe`) are only the example below. At a release tag, e.g. the oldest
supported one:

```sh
gh api "repos/Dolibarr/dolibarr/contents/htdocs/societe/class/api_thirdparties.class.php?ref=24.0.0" \
  --jq .content | base64 -d
```

Each public method is a route: its `@url` tag gives the HTTP method and the
path, its `@param` tags the query or body fields, `@throws` the errors.

## Review a new release

The weekly `dolibarr-api.yml` workflow compares the latest Dolibarr release
with `.github/dolibarr-api-version` and opens a `scope: client` issue
"Dolibarr API changes in <new>" when they differ, with the diff stat of the
files used by the tools, the other API files changed and the ChangeLog lines
naming the API, and starts the `integration.yml` workflow against the new
release (built from its tag when it has no official image yet; see the
[dolibarr-test](../dolibarr-test/SKILL.md) skill). Once the release is reviewed, set the version in
`.github/dolibarr-api-version` to it in the same PR as the tool fixes, or in
a `chore(client)` PR when nothing changes for us.

Fetch the two tags without history or file contents (a few seconds), in a
temporary directory:

```sh
cd "$(mktemp -d)" && git init -q
git fetch -q --depth=1 --filter=blob:none https://github.com/Dolibarr/dolibarr.git tag <old> tag <new>
git diff --stat <old> <new> -- ':(glob)htdocs/**/class/api_*.class.php'   # every module
git diff <old> <new> -- htdocs/societe/class/api_thirdparties.class.php  # one file, in full
git show <new>:ChangeLog    # the WARNING: section, and the lines naming the API
```

A change that affects a tool gets its own `fix(tools)` or `feat(tools)` change,
with a test. A change that the oldest supported version can't follow is
reported to the user, not worked around silently.
