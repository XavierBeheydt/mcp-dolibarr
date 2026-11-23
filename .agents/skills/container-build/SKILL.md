---
name: container-build
description: Build and run the container image with Podman. Use when changing the Containerfile, the dependencies, or checking the server runs in a container.
---

# Container build

Build from the project root; the image runs the streamable HTTP transport on
port 8000:

```sh
podman build -t mcp-dolibarr -f Containerfile .
podman run --rm --env-file .env -p 127.0.0.1:8000:8000 mcp-dolibarr
```

The endpoint is `http://127.0.0.1:8000/mcp`. The image has no
authentication of its own: never publish its port beyond localhost; expose
it only through a reverse proxy that authenticates, see
[docs/deployment.md](../../../docs/deployment.md).
