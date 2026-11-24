---
name: dolibarr-test
description: Run the integration tests against a disposable Dolibarr in containers. Use after changing a tool or the client, or to check a Dolibarr release.
---

# Dolibarr integration tests

The unit tests mock Dolibarr; the integration tests (`tests/integration`,
marker `integration`, left out of the default `pytest` run) call every tool,
the write tools included, on a real Dolibarr loaded with its demo data. They
need only a URL and an API key, so Podman or Docker both work.

## Cycle

From the project root, with `podman compose` or `docker compose`:

```sh
export DOLIBARR_VERSION=24.0.0   # 24.0.0 (oldest supported), 24.0.2, ...
podman compose -f tests/integration/compose.yml up -d --wait
export DOLIBARR_TEST_URL=http://127.0.0.1:8080/api/index.php
export DOLIBARR_TEST_API_KEY=integration-test-key
uv run python tests/integration/seed.py
uv run pytest -m integration
podman compose -f tests/integration/compose.yml down -v
```

- On its first start the image installs Dolibarr, loads the demo dump of the
  release (`dev/initdemo/mysqldump_dolibarr_<x.y>.0.sql`, downloaded, never
  committed), then `docker-init.d/setup.sh` sets the admin's API key and
  turns the Unalterable Logs module off. About a minute; `--wait` returns
  once the API answers with the key.
- `seed.py` adds what the demo data lacks (an apostrophe in a name, a
  supplier-only third party, a prospect) and the marker third party.
- `down -v` drops the database: the next `up` starts from the demo data again.
  Tests that write leave their objects behind until then.
- `DOLIBARR_TEST_PORT` changes the host port (default 8080).

## Never a real ERP

The tests refuse an instance without the marker third party, and
`DOLIBARR_TEST_URL` is never read from `.env`. Run `seed.py` only on the
compose instance: never on the maintainer's Dolibarr.

## A release without an official image

The official image lags behind the releases. When `dolibarr/dolibarr:<version>`
does not exist, build one from the release tag, then point the compose file at
it:

```sh
podman build -t localhost/dolibarr:24.0.3 --build-arg DOLIBARR_VERSION=24.0.3 \
  -f tests/integration/Containerfile tests/integration
export DOLIBARR_VERSION=24.0.3 DOLIBARR_IMAGE=localhost/dolibarr:24.0.3
```

The `Containerfile` takes the newest official image (`BASE_VERSION`) and
replaces its sources with the tag's: the tested code is the release's.

## In the CI

`.github/workflows/integration.yml` runs this cycle on every PR into `main`
(the release PR) for 24.0.0, 24.0.2 and the newest release, and on demand
(*Run workflow*, with a `dolibarr-version`). A version without an official
image is built from its tag; a version that is not a release fails at once.
The `Integration` job sums up the matrix: it is the check to require.
