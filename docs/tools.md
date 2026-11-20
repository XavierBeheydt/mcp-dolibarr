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

## Dolibarr API reference

Dolibarr 24 or later is supported. Before adding or changing a tool, check
its endpoint in the code of the oldest supported version, and what changed
since (see the [dolibarr-api](../.agents/skills/dolibarr-api/SKILL.md)
skill). Sources:

- The explorer of an instance, `<DOLIBARR_URL>/explorer` (Swagger UI, unless
  `API_EXPLORER_DISABLED` is set), and its `explorer/swagger.json`: the
  endpoints of that version and of its enabled modules.
- The code of each endpoint in
  [Dolibarr/dolibarr](https://github.com/Dolibarr/dolibarr), at the release
  tag (table below).
- The [ChangeLog](https://github.com/Dolibarr/dolibarr/blob/develop/ChangeLog):
  the `WARNING:` section of each version lists the breaking changes, the REST
  API ones included, and `FIX:` lines name the API fixes.
- The wiki page [Module Web Services API REST
  (developer)](https://wiki.dolibarr.org/index.php/Module_Web_Services_API_REST_%28developer%29).

| Endpoint | Source |
| --- | --- |
| `status` | `htdocs/api/class/api_status.class.php` |
| `thirdparties` | `htdocs/societe/class/api_thirdparties.class.php` |
| `contacts` | `htdocs/societe/class/api_contacts.class.php` |
| `products` | `htdocs/product/class/api_products.class.php` |
| `projects` | `htdocs/projet/class/api_projects.class.php` |
| `proposals` | `htdocs/comm/propal/class/api_proposals.class.php` |
| `orders` | `htdocs/commande/class/api_orders.class.php` |
| `invoices` | `htdocs/compta/facture/class/api_invoices.class.php` |
