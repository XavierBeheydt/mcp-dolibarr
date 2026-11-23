# Deployment

The container serves the streamable HTTP transport on port 8000, with no
authentication of its own: expose it only through a reverse proxy that
authenticates. Build and run it with the
[container-build](../.agents/skills/container-build/SKILL.md) skill.

## Behind a reverse proxy

A reverse proxy gives the server its public URL, such as
`https://mcp.example.com/dolibarr`, and handles TLS. The server itself always
answers on `/mcp`, so the proxy rewrites the public path to it. With Traefik,
as labels of the service:

```yaml
labels:
  - traefik.enable=true
  - traefik.http.routers.dolibarr-mcp.rule=Host(`mcp.example.com`) && PathPrefix(`/dolibarr`)
  - traefik.http.routers.dolibarr-mcp.entrypoints=websecure
  - traefik.http.routers.dolibarr-mcp.tls=true
  - traefik.http.routers.dolibarr-mcp.middlewares=dolibarr-mcp-path
  - traefik.http.middlewares.dolibarr-mcp-path.replacepathregex.regex=^/dolibarr/?$$
  - traefik.http.middlewares.dolibarr-mcp-path.replacepathregex.replacement=/mcp
  - traefik.http.services.dolibarr-mcp.loadbalancer.server.port=8000
```

- Anchor the regex: a prefix rewrite turns `/dolibarr/` into `/mcp/`, which the
  server redirects to `/mcp`, a path the proxy does not route.
- The responses stream: Traefik does not buffer them by default. With nginx,
  set `proxy_buffering off`.
- Checked with Traefik v3 and a rewrite to `/mcp`, over HTTP: an MCP session
  lists the tools and calls one. The labels above are the same options as the
  file configuration tested, and were not run themselves.
