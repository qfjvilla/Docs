import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
from sync import sync, init_db, DB

st.set_page_config(page_title="Resumen de correos", layout="wide")
st.title("📬 Resumen diario de correos")

init_db().close()

if st.sidebar.button("🔄 Actualizar ahora"):
    with st.spinner("Leyendo Outlook..."):
        sync()
dias = st.sidebar.slider("Últimos días", 1, 7, 1)
solo_pendientes = st.sidebar.checkbox("Ocultar los marcados como hechos", value=True)

con = sqlite3.connect(DB)
df = pd.read_sql("SELECT * FROM correos ORDER BY fecha DESC", con)
if df.empty:
    st.info("No hay correos todavía. Pulsa «Actualizar ahora» en la barra lateral.")
    st.stop()

df["fecha"] = pd.to_datetime(df["fecha"], utc=True)
df = df[df["fecha"] >= pd.Timestamp.now(tz="UTC") - timedelta(days=dias)]
if solo_pendientes:
    df = df[df["hecho"] == 0]

categorias = ["🔴 Urgente", "✅ Acción requerida", "📌 Actividad asignada",
              "💳 Facturas/Pagos", "🔐 Seguridad", "📢 Publicidad", "📄 Informativo"]

cols = st.columns(len(categorias))
for col, cat in zip(cols, categorias):
    col.metric(cat, int(df["categorias"].str.contains(cat, regex=False).sum()))
st.caption(f"{len(df)} correos · {int((df['leido'] == 0).sum())} sin leer · "
           f"actualizado {datetime.now():%d/%m/%Y %H:%M}")

tabs = st.tabs(categorias)
for tab, cat in zip(tabs, categorias):
    with tab:
        sub = df[df["categorias"].str.contains(cat, regex=False)]
        if sub.empty:
            st.write("Nada por aquí 🎉")
        for _, r in sub.iterrows():
            with st.container(border=True):
                c1, c2, c3 = st.columns([6, 1.3, 1.3])
                punto = "🔵 " if r["leido"] == 0 else ""
                c1.markdown(f"**{punto}{r['asunto']}**  \n"
                            f"{r['nombre'] or r['remitente']} · {r['fecha']:%d/%m %H:%M}")
                c1.caption((r["resumen"] or "")[:200])
                c2.link_button("Abrir en Outlook", r["link"])
                if c3.button("✔ Hecho", key=f"{cat}-{r['id']}"):
                    con.execute("UPDATE correos SET hecho=1 WHERE id=?", (r["id"],))
                    con.commit()
                    st.rerun()
