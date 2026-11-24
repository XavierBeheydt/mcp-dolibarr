# Copyright (c) 2026 Beheydt.DEV <xavier.beheydt@gmail.com>
# SPDX-License-Identifier: MIT
#
# Run by the Dolibarr image after its first install, the demo data loaded:
# - the API key of the admin user (Dolibarr accepts a key stored in clear);
# - the Unalterable Logs module off: its HMAC key in the demo data was
#   encrypted with another instance's key, so validating an invoice fails.

mysql -u "$DOLI_DB_USER" -p"$DOLI_DB_PASSWORD" -h "$DOLI_DB_HOST" -P "$DOLI_DB_HOST_PORT" \
  "$DOLI_DB_NAME" -e "
    UPDATE llx_user SET api_key = '$DOLI_TEST_API_KEY' WHERE login = '$DOLI_ADMIN_LOGIN';
    DELETE FROM llx_const WHERE name LIKE 'MAIN_MODULE_BLOCKEDLOG%';"
