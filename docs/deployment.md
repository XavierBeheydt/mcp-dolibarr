# Deployment

The container serves the streamable HTTP transport on port 8000, with no
authentication of its own: expose it only through a reverse proxy that
authenticates. Build and run it with the
[container-build](../.agents/skills/container-build/SKILL.md) skill.

## Behind a reverse proxy

The proxy handles TLS and forwards to port 8000. With Traefik, these labels on
the service give `https://mcp.example.com/mcp`:

```yaml
labels:
  - traefik.enable=true
  - traefik.http.routers.mcp.rule=Host(`mcp.example.com`) && PathPrefix(`/mcp`)
  - traefik.http.routers.mcp.entrypoints=websecure
  - traefik.http.routers.mcp.tls=true
  - traefik.http.services.mcp.loadbalancer.server.port=8000
```

- For another path, set `MCP_PATH` and the same `PathPrefix`.
- Give the clients the URL without a trailing slash: behind a TLS proxy, the
  server redirects `/mcp/` to an `http` URL.
- The responses stream: Traefik does not buffer them. With nginx, set
  `proxy_buffering off`.
