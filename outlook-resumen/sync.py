import sqlite3
from fetch import fetch_emails
from classify import clasificar

DB = "correos.db"


def init_db():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS correos (
        id TEXT PRIMARY KEY, asunto TEXT, remitente TEXT, nombre TEXT,
        fecha TEXT, resumen TEXT, link TEXT, leido INTEGER,
        adjuntos INTEGER, categorias TEXT, hecho INTEGER DEFAULT 0)""")
    return con


def sync(days=2):
    con = init_db()
    total = 0
    for e in fetch_emails(days=days):
        cats = clasificar(e)
        sender = e["from"]["emailAddress"]
        con.execute(
            """INSERT INTO correos (id, asunto, remitente, nombre, fecha, resumen, link, leido, adjuntos, categorias)
               VALUES (?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(id) DO UPDATE SET leido=excluded.leido, categorias=excluded.categorias""",
            (e["id"], e["subject"], sender["address"], sender.get("name", ""),
             e["receivedDateTime"], e["bodyPreview"], e["webLink"], int(e["isRead"]),
             int(e["hasAttachments"]), ",".join(cats)))
        total += 1
    con.commit()
    con.close()
    print(f"Sincronizados {total} correos")
    return total


if __name__ == "__main__":
    sync()
