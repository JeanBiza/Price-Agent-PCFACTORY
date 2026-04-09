# 🤖 Price Agent PCFactory

Aplicación web que monitorea precios de productos en **PCFactory** y envía alertas automáticas por **Telegram** y **Email** cuando el precio cambia.

## ✨ Características

- 📦 Seguimiento de múltiples productos simultáneamente
- 🔔 Alertas automáticas por Telegram y Email al detectar cambios de precio
- 📊 Historial de precios por producto
- 👤 Sistema de usuarios con registro, verificación por email y login
- ☁️ Desplegado en la nube con base de datos PostgreSQL
- ⏰ Monitoreo automático semanal via GitHub Actions

## 🛠️ Stack tecnológico

| Componente | Tecnología |
|---|---|
| Backend | Python + Flask |
| Base de datos | PostgreSQL (Supabase) |
| Frontend | HTML + Bootstrap 5 |
| Alertas email | Resend API |
| Alertas Telegram | Telegram Bot API |
| Hosting | Render |
| Monitoreo automático | GitHub Actions |

## 📁 Estructura del proyecto

```
Price-Agent/
├── app.py              # Servidor Flask y rutas
├── database.py         # Conexión y operaciones con PostgreSQL
├── scraper.py          # Extracción de precios desde API de PCFactory
├── notifier.py         # Envío de alertas por Telegram y Email
├── monitor.py          # Script de monitoreo (ejecutado por GitHub Actions)
├── tools.py            # Utilidades (envío de código de verificación)
├── templates/          # Templates HTML con Jinja2
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── verify.html
│   ├── profile.html
│   └── history.html
├── .github/
│   └── workflows/
│       └── monitor.yml # Configuración de GitHub Actions
├── requirements.txt
├── .env.example
└── .gitignore
```

## ⚙️ Instalación local

### 1. Clonar el repositorio

```bash
git clone https://github.com/JeanBiza/Price-Agent-PCFACTORY.git
cd Price-Agent-PCFACTORY
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copia `.env.example` a `.env` y completa los valores:

```bash
cp .env.example .env
```

```env
TOKEN=          # Token de tu bot de Telegram (@BotFather)
EMAIL_SENDER=   # Tu email de Gmail
EMAIL_PASSWORD= # Contraseña de aplicación de Gmail
RESEND_API_KEY= # API key de Resend (resend.com)
SECRET_KEY=     # Clave secreta para Flask sessions
DATABASE_URL=   # URL de conexión a PostgreSQL (Supabase)
```

### 4. Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## 🔑 Configuración de servicios externos

### Telegram Bot
1. Busca `@BotFather` en Telegram
2. Envía `/newbot` y sigue los pasos
3. Copia el token generado a `TOKEN` en el `.env`
4. Para obtener tu `chat_id`, envía un mensaje a tu bot y visita:
   `https://api.telegram.org/bot<TOKEN>/getUpdates`

### Gmail (contraseña de aplicación)
1. Activa la verificación en dos pasos en tu cuenta Google
2. Ve a **Seguridad → Contraseñas de aplicación**
3. Genera una contraseña para "Correo"
4. Cópiala a `EMAIL_PASSWORD` en el `.env`

### Resend
1. Crea una cuenta en [resend.com](https://resend.com)
2. Genera una API key
3. Cópiala a `RESEND_API_KEY` en el `.env`

### Supabase
1. Crea un proyecto en [supabase.com](https://supabase.com)
2. Ve a **Settings → Database → Connection string**
3. Copia la URL del connection pooler a `DATABASE_URL` en el `.env`

## 🚀 Deploy en Render

1. Conecta tu repositorio de GitHub en [render.com](https://render.com)
2. Crea un nuevo **Web Service** con la siguiente configuración:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
3. Agrega todas las variables de entorno en la sección **Environment**

## ⏰ Monitoreo automático con GitHub Actions

El archivo `.github/workflows/monitor.yml` ejecuta el monitoreo automáticamente **todos los lunes a las 12:00 UTC**.

Para configurarlo, agrega los siguientes **secrets** en tu repositorio:
`Settings → Secrets and variables → Actions`

```
TOKEN
EMAIL_PASSWORD
EMAIL_SENDER
RESEND_API_KEY
DATABASE_URL
```

También puedes ejecutarlo manualmente desde la pestaña **Actions** de tu repositorio usando el botón **Run workflow**.

## 🌐 Demo

[price-agent-pcfactory.onrender.com](https://price-agent-pcfactory.onrender.com)

## 📝 Uso

1. **Regístrate** con tu email y verifica tu cuenta
2. **Agrega tu Telegram ID** en la sección de perfil para recibir alertas
3. **Agrega productos** pegando la URL de cualquier producto de PCFactory
4. **Define un umbral** de precio de referencia
5. Cada lunes el sistema consulta los precios y te notifica si hubo cambios

## 👨‍💻 Autor

Jean Biza — [@JeanBiza](https://github.com/JeanBiza)
