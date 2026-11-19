# Tools

The MCP tools, and the Dolibarr REST conventions they rely on. The server
also sends the model short instructions (`INSTRUCTIONS` in `server.py`):
`sqlfilters` syntax.

## Read

| Tool | Dolibarr endpoint | Purpose |
| --- | --- | --- |
| `get_status` | `GET status` | Check the connection and the API key |
| `get_object` | `GET <kind>s/{id}` | Full object: thirdparty, contact, product, project, proposal, order, invoice |
| `dolibarr_get` | `GET <path>` | Any other read |

## Write (`DOLIBARR_ALLOW_WRITE=true`)

| Tool | Dolibarr endpoint | Annotation |
| --- | --- | --- |
| `dolibarr_request` | any method and path | destructive |

## Dolibarr REST conventions

- Authentication: the `DOLAPIKEY` header.
- An empty list is a `404`, which the client turns into `[]`.
