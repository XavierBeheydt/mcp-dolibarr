# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT
"""Add to a disposable Dolibarr the cases its demo data lacks, and the marker the tests require.

Usage: DOLIBARR_TEST_URL=... DOLIBARR_TEST_API_KEY=... uv run python tests/integration/seed.py
Run it only on the instance of `tests/integration/compose.yml`: the marker tells the
integration tests that they may write there.
"""

import os

import httpx

MARKER = "mcp-dolibarr integration marker"

THIRDPARTIES = [
    {"name": MARKER, "client": 0, "fournisseur": 0},
    {"name": "L'Atelier d'Annecy", "client": 1, "fournisseur": 0},
    {"name": "Supplier Only Ltd", "client": 0, "fournisseur": 1},
    {"name": "Prospect Corp", "client": 2, "fournisseur": 0},
]


def main() -> None:
    url, key = os.environ["DOLIBARR_TEST_URL"], os.environ["DOLIBARR_TEST_API_KEY"]
    with httpx.Client(base_url=url, headers={"DOLAPIKEY": key}, timeout=30) as http:
        for fields in THIRDPARTIES:
            name = fields["name"].replace("'", "_")
            found = http.get("thirdparties", params={"sqlfilters": f"(t.nom:like:'{name}')"})
            if found.status_code == 200 and found.json():
                continue
            # "auto": the demo data numbers the customer and supplier codes.
            codes = {"code_client": "auto", "code_fournisseur": "auto"}
            http.post("thirdparties", json=fields | codes).raise_for_status()
            print(f"Created {fields['name']}")


if __name__ == "__main__":
    main()
