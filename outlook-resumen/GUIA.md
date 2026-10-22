# Guía paso a paso: Resumen diario de correos de Outlook

Al terminar tendrás un dashboard en tu navegador con tus correos clasificados
(urgentes, acciones, actividades, facturas, publicidad...) y un botón para
abrir cada uno en Outlook.

Tiempo estimado: 20–30 minutos. Solo hace falta hacerlo una vez.

---

## Paso 1. Comprueba Python

Abre VS Code → menú **Terminal → Nueva terminal** y escribe:

```powershell
python --version
```

Debe mostrar Python 3.9 o superior. Si no, instálalo desde https://www.python.org
(marca la casilla **Add Python to PATH**).

## Paso 2. Abre esta carpeta e instala las librerías

En VS Code: **Archivo → Abrir carpeta…** y elige `outlook-resumen`.
En la terminal (PowerShell) ejecuta, línea por línea:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

> Si PowerShell dice que "la ejecución de scripts está deshabilitada", ejecuta
> una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y repite.

Sabrás que el entorno está activo porque verás `(.venv)` al inicio de la línea.

## Paso 3. Registra la aplicación en Microsoft (permiso para leer tu correo)

Es el paso más importante: Microsoft debe saber que tu programa tiene permiso
para leer tu bandeja de entrada. Solo lectura, nunca puede enviar ni borrar.

1. Entra a https://entra.microsoft.com con la misma cuenta de tu Outlook.
   (Si tienes cuenta personal Hotmail/Outlook.com y no te deja entrar, usa
   https://portal.azure.com y busca "Registros de aplicaciones".)
2. Menú **Identidad → Aplicaciones → Registros de aplicaciones → Nuevo registro**.
3. Rellena:
   - **Nombre:** `ResumenCorreos`
   - **Tipos de cuenta compatibles:** *Cuentas en cualquier directorio
     organizativo y cuentas personales de Microsoft*
   - **URI de redirección:** plataforma *Cliente público/nativo (móvil y
     escritorio)* y valor `http://localhost`
4. Pulsa **Registrar**.
5. En la pantalla de resumen copia el **Id. de aplicación (cliente)**
   (un código tipo `a1b2c3d4-....`).
6. Menú **Permisos de API → Agregar un permiso → Microsoft Graph →
   Permisos delegados** → busca y marca **Mail.Read** → **Agregar permisos**.
7. Menú **Autenticación** → baja hasta **Permitir flujos de clientes públicos**
   y ponlo en **Sí** → **Guardar**.

> Cuenta de empresa/colegio: si el paso 6 muestra "Se requiere consentimiento
> de administrador", tendrás que pedírselo a TI.

## Paso 4. Configura tu Id de cliente

1. Copia el archivo `.env.example` y renómbralo a `.env`
   (en PowerShell: `copy .env.example .env`).
2. Ábrelo y pega tu Id:

```
CLIENT_ID=a1b2c3d4-xxxx-xxxx-xxxx-xxxxxxxxxxxx
TENANT_ID=common
```

Guarda el archivo.

## Paso 5. Prueba la conexión con tu correo

```powershell
python fetch.py
```

- Se abrirá el navegador: inicia sesión con tu cuenta de Outlook y pulsa
  **Aceptar** cuando pida el permiso de lectura.
- En la terminal deberían aparecer los asuntos de tus últimos correos.

Esto solo pide login la primera vez; después queda guardado en
`token_cache.json`.

**Problemas frecuentes**

| Mensaje | Qué hacer |
|---|---|
| `Falta CLIENT_ID` | Revisa el paso 4 (nombre `.env`, sin espacios ni comillas). |
| `AADSTS700016` | El Id de cliente está mal copiado. |
| `AADSTS50194` / cuenta no encontrada | En el paso 3.3 elige tipos de cuenta que incluyan personales, o pon el ID de tu directorio en `TENANT_ID`. |
| `AADSTS65001` | Falta consentimiento: repite el login y acepta, o pide el consentimiento de admin. |
| `AADSTS7000218` | Activa «Permitir flujos de clientes públicos» (paso 3.7). |
| `403` / `ErrorAccessDenied` | Falta el permiso `Mail.Read` (paso 3.6). |

## Paso 6. Descarga y clasifica tus correos

```powershell
python sync.py
```

Debe imprimir `Sincronizados N correos`. Se crea `correos.db` con todo clasificado.

## Paso 7. Abre el dashboard

```powershell
streamlit run dashboard.py
```

(o haz doble clic en `iniciar_dashboard.bat`). Se abre
http://localhost:8501 con:

- Contadores por categoría arriba.
- Una pestaña por categoría: Urgente, Acción requerida, Actividad asignada,
  Facturas/Pagos, Seguridad, Publicidad, Informativo.
- Por cada correo: botón **Abrir en Outlook** (te lleva al mensaje) y botón
  **✔ Hecho** (lo oculta cuando ya lo resolviste).
- Barra lateral: **Actualizar ahora** y selector de días.

## Paso 8. Que se actualice solo cada mañana

1. Abre el **Programador de tareas** de Windows (búscalo en el menú Inicio).
2. **Crear tarea básica…** → nombre `Sync correos`.
3. Desencadenador: **Diariamente**, a las 7:30.
4. Acción: **Iniciar un programa** → elige el archivo `sync.bat` de esta carpeta.
5. Finalizar.

Cada mañana tendrás el resumen listo; solo abre `iniciar_dashboard.bat`.

## Paso 9. Personaliza la clasificación

Abre `classify.py`. Cada categoría es una lista de palabras separadas por `|`.
Añade las palabras que usan tus correos reales (nombres de tus clientes, de tu
jefe, de tu herramienta de tareas, etc.). Luego pulsa **Actualizar ahora**.

## Mejoras futuras

- Clasificar con IA (API de Claude) para más precisión. Ojo: el texto de
  los correos se enviaría a un servicio externo.
- Enviarte el resumen por correo o Teams.
- Aprender de tus correcciones (remitentes que siempre son publicidad).

## Seguridad

`.env`, `token_cache.json` y `correos.db` son privados. Ya están en
`.gitignore`; no los subas a internet ni los compartas.
