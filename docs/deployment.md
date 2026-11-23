# Deployment

The container serves the streamable HTTP transport on port 8000, with no
authentication of its own: expose it only through a reverse proxy that
authenticates. Build and run it with the
[container-build](../.agents/skills/container-build/SKILL.md) skill.

## Behind a reverse proxy

A reverse proxy gives the server its public URL, such as
`https://mcp.example.com/dolibarr`, and handles TLS. Set `MCP_PATH` to the
public path, and the proxy only forwards. With Traefik, `MCP_PATH=/dolibarr` in
the environment of the service and these labels:

```yaml
labels:
  - traefik.enable=true
  - traefik.http.routers.dolibarr-mcp.rule=Host(`mcp.example.com`) && PathPrefix(`/dolibarr`)
  - traefik.http.routers.dolibarr-mcp.entrypoints=websecure
  - traefik.http.routers.dolibarr-mcp.tls=true
  - traefik.http.services.dolibarr-mcp.loadbalancer.server.port=8000
```

- The server answers on `/dolibarr` only, not on `/mcp`. Give the clients the
  URL without a trailing slash: the server redirects `/dolibarr/` to
  `/dolibarr`, with the scheme it sees, which is `http` behind a TLS proxy.
- To keep the default `/mcp` instead, rewrite the public path to it, with an
  anchored regex so that the trailing slash works too:
  `replacepathregex.regex=^/dolibarr/?$$` and `replacepathregex.replacement=/mcp`
  (a middleware of the same router). An unanchored prefix rewrite turns
  `/dolibarr/` into `/mcp/`, which the server redirects to a path the proxy
  does not route.
- The responses stream: Traefik does not buffer them by default. With nginx,
  set `proxy_buffering off`.
- Checked with Traefik v3 over HTTP, both ways (`MCP_PATH` with a `Host` rule
  and no rewrite, and the rewrite to `/mcp`): an MCP session lists the tools
  and calls one. The labels are the same options as the file configuration
  that was run, and were not run themselves.
