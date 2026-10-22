import os
import msal
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('TENANT_ID', 'common')}"
SCOPES = ["Mail.Read"]
CACHE_FILE = "token_cache.json"


def get_token():
    if not CLIENT_ID or CLIENT_ID.startswith("pega-aqui"):
        raise SystemExit("Falta CLIENT_ID en el archivo .env (ver GUIA.md, Paso 3).")

    cache = msal.SerializableTokenCache()
    if os.path.exists(CACHE_FILE):
        cache.deserialize(open(CACHE_FILE).read())

    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)
    accounts = app.get_accounts()
    result = app.acquire_token_silent(SCOPES, account=accounts[0]) if accounts else None
    if not result:
        result = app.acquire_token_interactive(SCOPES)  # abre el navegador la 1ª vez

    if "access_token" not in result:
        raise SystemExit(f"No se pudo iniciar sesión: {result.get('error_description', result)}")

    if cache.has_state_changed:
        open(CACHE_FILE, "w").write(cache.serialize())
    return result["access_token"]
