import re

# Edita estas reglas a tu gusto: cada categoría es una expresión regular.
REGLAS = {
    "🔴 Urgente": r"urgente|urgent|asap|inmediat|hoy mismo|vence hoy|deadline|último aviso|importante",
    "✅ Acción requerida": r"por favor|favor de|necesito que|puedes|podrías|confirma|aprobar|aprobación|revisar|responde|action required|please",
    "📌 Actividad asignada": r"te asign|asignad|tarea|task|assigned|planner|jira|trello|asana|reunión|invitación|meeting|calendario|agenda",
    "📢 Publicidad": r"oferta|descuento|% ?dto|promoci|newsletter|unsubscribe|darse de baja|cancelar suscripci|suscripci|boletín|sale|cupón|black friday",
    "💳 Facturas/Pagos": r"factura|invoice|pago|payment|recibo|vencimiento|cobro",
    "🔐 Seguridad": r"contraseña|password|código de verificación|verification code|inicio de sesión|security alert|2fa",
}


def clasificar(email):
    texto = f"{email['subject']} {email['bodyPreview']}".lower()
    sender = email["from"]["emailAddress"]["address"].lower()
    cats = [c for c, patron in REGLAS.items() if re.search(patron, texto)]

    if email.get("importance") == "high" and "🔴 Urgente" not in cats:
        cats.append("🔴 Urgente")
    if email.get("flag", {}).get("flagStatus") == "flagged":
        cats.append("✅ Acción requerida")
    if re.search(r"no-?reply|newsletter|marketing|mailer", sender) and "📢 Publicidad" not in cats:
        cats.append("📢 Publicidad")

    # Publicidad no debe contar como urgente solo por una palabra suelta
    if "📢 Publicidad" in cats and "🔴 Urgente" in cats and email.get("importance") != "high":
        cats.remove("🔴 Urgente")

    return cats or ["📄 Informativo"]
