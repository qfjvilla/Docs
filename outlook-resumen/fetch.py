from datetime import datetime, timedelta, timezone
import requests
from auth import get_token

GRAPH = "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages"


def fetch_emails(days=2):
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    params = {
        "$filter": f"receivedDateTime ge {since}",
        "$orderby": "receivedDateTime desc",
        "$top": 50,
        "$select": "id,subject,from,receivedDateTime,bodyPreview,webLink,importance,isRead,flag,hasAttachments",
    }
    headers = {"Authorization": f"Bearer {get_token()}"}
    url, emails = GRAPH, []
    while url:
        r = requests.get(url, headers=headers, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        emails += data["value"]
        url, params = data.get("@odata.nextLink"), None  # paginación
    return emails


if __name__ == "__main__":
    # Prueba rápida: muestra los asuntos de los últimos correos
    for e in fetch_emails(days=1)[:10]:
        print("-", e["subject"])
