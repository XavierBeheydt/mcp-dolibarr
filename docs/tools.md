# Tools

The MCP tools, and the Dolibarr REST conventions they rely on. The server
also sends the model short instructions (`INSTRUCTIONS` in `server.py`):
`sqlfilters` syntax and status codes.

## Read

| Tool | Dolibarr endpoint | Purpose |
| --- | --- | --- |
| `get_status` | `GET status` | Check the connection and the API key |
| `get_object` | `GET <kind>s/{id}` | Full object: thirdparty, contact, product, project, proposal, order, invoice |
| `search_thirdparties` | `GET thirdparties` | By name or alias, and role (customer, prospect, supplier) |
| `search_products` | `GET products` | By reference or label, and type (product, service) |
| `list_sales_documents` | `GET proposals`, `orders`, `invoices` | By third party, status, `sqlfilters` |
| `dolibarr_get` | `GET <path>` | Any other read |

## Write (`DOLIBARR_ALLOW_WRITE=true`)

| Tool | Dolibarr endpoint | Annotation |
| --- | --- | --- |
| `create_thirdparty` | `POST thirdparties` | create |
| `create_sales_document` | `POST <kind>s`, then one `POST` per line (see below) | create (draft) |
| `add_sales_document_line` | `POST proposals/{id}/line`, `orders/{id}/lines`, `invoices/{id}/lines` | create |
| `validate_sales_document` | `POST <kind>s/{id}/validate` | destructive: final reference |
| `dolibarr_request` | any method and path | destructive |

The `*_sales_document*` tools handle the sales documents, which are records with
lines, amounts and a status: proposals, orders and invoices. Not the PDF files Dolibarr
generates for them, which its `documents` API serves and no tool covers yet.

## Dolibarr REST conventions

- Authentication: the `DOLAPIKEY` header.
- Lists take `limit`, `page`, `sortfield`, `sortorder`, `sqlfilters`, and
  `properties` (the fields to return; ignored by old Dolibarr versions).
- An empty list of third parties is a `404` "No … found", which the client turns
  into `[]`; the other lists answer `200` and `[]`. Any other `404` stays an
  error: Dolibarr serves the routes of enabled modules only.
- A `POST` that creates an object returns its numeric id.
- One line is added with `POST proposals/{id}/line` but `POST orders/{id}/lines`
  and `invoices/{id}/lines`: `proposals/{id}/lines` takes a list of lines.
- A third party is created with `code_client` / `code_fournisseur` set to
  `auto`: Dolibarr numbers the code when its code module requires one (as the
  demo data does), and leaves it empty otherwise.
- Dates are Unix timestamps; `create_sales_document` sends noon UTC of the given
  day, so the date is right in any server time zone.
- `sqlfilters` values sit in single quotes and can't escape one: `like()`
  replaces a quote in the searched text with the `_` wildcard.

## Dolibarr modules

A tool works only if its Dolibarr module is enabled; otherwise Dolibarr answers `404`
and the tool reports it.

| Resource | Module |
| --- | --- |
| `thirdparties` | Third Parties |
| `products` | Products or Services |
| `proposals` | Proposals |
| `orders` | Sales Orders |
| `invoices` | Invoices |
| every endpoint | API / Web services (REST server) |

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
