<<<<<<< HEAD
# 🤖 EdgarAI — Asistente de Soporte IT

![EdgarAI](static/iaconbarba.png)

EdgarAI es un chatbot de soporte IT inteligente con interfaz profesional, sistema de tickets integrado y soporte para imágenes.

---

## 📁 Estructura del proyecto

```
edgarai/
├── app.py                  # Servidor Flask (backend)
├── requirements.txt        # Dependencias Python
├── .env.example            # Plantilla de variables de entorno
├── .env                    # Tu configuración real (créalo tú)
├── templates/
│   └── index.html          # Interfaz web completa
└── static/
    └── iaconbarba.png      # Avatar de EdgarAI
=======
# 🤖 EdgarAI — Asistente de Soporte IT con Inteligencia Artificial

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-00BCD4?style=flat&logo=flask&logoColor=white)
![OpenAI](https://img.shields.io/badge/GPT--4o-OpenAI-10A37F?style=flat&logo=openai&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat&logo=postgresql&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-F7DF1E?style=flat&logo=javascript&logoColor=black)
![Status](https://img.shields.io/badge/Status-En%20producción-00d68f?style=flat)

> Sistema completo de soporte técnico corporativo donde los usuarios resuelven problemas técnicos en tiempo real con ayuda de IA, levantan tickets y dan seguimiento desde cualquier dispositivo.

---

## ✨ ¿Qué hace EdgarAI?

| Funcionalidad | Descripción |
|---|---|
| 💬 **Chat con IA** | Conversación en tiempo real con GPT-4o para diagnóstico técnico |
| 📸 **Análisis de imágenes** | El usuario sube una captura y la IA identifica el error automáticamente |
| 🎫 **Gestión de tickets** | Crear, seguir y actualizar tickets con categoría, prioridad e historial |
| 👥 **Sistema de roles** | Administrador y Operador con permisos y vistas diferenciadas |
| 📊 **Panel Admin** | Dashboard estilo ServiceNow con filtros, buscador y timeline por ticket |
| 📱 **Multi-dispositivo** | Compatible con Desktop, iPhone y Android |

---

## 🛠️ Stack Tecnológico

```
Backend        →  Python 3.11 + Flask + Flask-CORS + Flask-Session
IA             →  OpenAI GPT-4o (chat + vision)
Base de datos  →  PostgreSQL 16 + psycopg2
Frontend       →  HTML5 + CSS3 + JavaScript Vanilla
Auth           →  Flask Sessions + SHA-256 password hashing
Admin DB       →  pgAdmin
Tunnel         →  ngrok (exposición local a internet)
Config         →  python-dotenv
>>>>>>> 8282c5278f1dae7f59bbaa943680d9370cde41b1
```

---

<<<<<<< HEAD
## 🚀 Instalación rápida

### 1. Clonar / descomprimir el proyecto
```bash
unzip edgarai.zip
cd edgarai
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar API Key
```bash
# Copia el archivo de ejemplo
cp .env.example .env

# Abre .env y reemplaza con tu API key real de Anthropic
# ANTHROPIC_API_KEY=sk-ant-TU-CLAVE-AQUI
```

> Obtén tu API key gratis en: https://console.anthropic.com

### 5. Ejecutar el servidor
=======
## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────┐
│                     FRONTEND                        │
│         HTML5 / CSS3 / JavaScript Vanilla           │
│     (Responsive — Desktop, iPhone, Android)         │
└──────────────────────┬──────────────────────────────┘
                       │  HTTP / REST API
┌──────────────────────▼──────────────────────────────┐
│                  BACKEND — Flask                    │
│                                                     │
│  /auth/*     →  Login, Register, Reset Password     │
│  /ask        →  Chat con GPT-4o (texto + imagen)    │
│  /tickets/*  →  CRUD tickets + historial estados    │
│  /admin/*    →  Panel admin (solo rol admin)        │
│                                                     │
│  Flask-Session  →  Autenticación y manejo sesiones  │
│  Roles          →  admin | operador                 │
└───────────┬─────────────────────┬───────────────────┘
            │                     │
┌───────────▼──────┐   ┌──────────▼────────────────┐
│   PostgreSQL     │   │       OpenAI API           │
│                  │   │                            │
│  usuarios        │   │  GPT-4o (texto)            │
│  tickets         │   │  GPT-4o Vision (imágenes)  │
│  conversaciones  │   │                            │
└──────────────────┘   └────────────────────────────┘
```

---

## 🔐 Sistema de Roles y Seguridad

EdgarAI implementa control de acceso basado en roles (**RBAC**):

### Administrador
- Ve **todos** los tickets del sistema con filtros y buscador
- Accede al historial completo de estados de cada ticket
- Gestiona usuarios y puede cambiar estados
- Ve todas las conversaciones del sistema

### Operador
- Ve **únicamente sus propios** tickets y conversaciones
- Puede crear tickets y chatear con la IA
- No tiene acceso al panel de administración ni a datos de otros usuarios

### Seguridad implementada
- Contraseñas hasheadas con **SHA-256**
- Sesiones protegidas con **secret key** configurable
- Decorador `@login_required` en todas las rutas protegidas
- Endpoint de **reset de contraseña** con validación
- Fallback a memoria si PostgreSQL no está disponible

---

## 🚀 Instalación y uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/edgarai.git
cd edgarai
```

### 2. Instalar dependencias
```bash
pip install flask flask-cors openai pillow python-dotenv psycopg2-binary
```

### 3. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto:
```env
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://usuario:password@localhost:5432/edgarai
SECRET_KEY=tu_clave_secreta_aqui
OPENAI_MODEL=gpt-4o
PORT=5000
DEBUG=true
```

### 4. Inicializar la base de datos
El sistema crea las tablas automáticamente al arrancar.
>>>>>>> 8282c5278f1dae7f59bbaa943680d9370cde41b1
```bash
python app.py
```

<<<<<<< HEAD
### 6. Abrir en el navegador
```
http://localhost:5000
=======
### 5. Acceder al sistema
```
http://localhost:5000

Usuario por defecto:
  user: admin
  pass: admin123
>>>>>>> 8282c5278f1dae7f59bbaa943680d9370cde41b1
```

---

<<<<<<< HEAD
## ✨ Funcionalidades

### 💬 Chat con IA
- Respuestas inteligentes con Claude (Anthropic)
- Soporte para adjuntar imágenes
- Historial de conversación
- Exportar conversación en .txt

### 🎫 Sistema de Tickets
- **Nombre del solicitante**
- **Resumen del problema**
- **Categoría** (14 categorías corporativas)
- **Subcategoría** dinámica según la categoría
- **Área / Departamento** (14 áreas)
- **Equipo / Activo afectado**
- **Prioridad visual** (1-Baja | 2-Normal | 3-Media | 4-Urgente)
- **Descripción detallada**
- Historial de tickets en sidebar
- Toast de confirmación

### 📱 Mobile-first
- Sidebar deslizable con botón hamburguesa
- Diseño responsive completo
- Input adaptado a pantallas pequeñas

---

## 🎨 Diseño
- Tema oscuro premium con acento cyan/purple
- Fuentes Syne + DM Sans
- Animaciones suaves
- Avatar de EdgarAI en el chat

---

## 🔧 Producción (Gunicorn)
```bash
gunicorn app:app --workers 4 --bind 0.0.0.0:5000
=======
## 📁 Estructura del Proyecto

```
edgarai/
│
├── app.py                  # Backend principal — rutas y lógica
├── .env                    # Variables de entorno (no incluido en repo)
├── requirements.txt        # Dependencias del proyecto
│
├── templates/
│   ├── login.html          # Página de autenticación
│   ├── index.html          # Chat principal con EdgarAI
│   └── admin.html          # Panel de administración
│
└── static/
    ├── edgarai_avatar.jpg  # Avatar del asistente
    └── iaconbarba.png      # Logo del sistema
>>>>>>> 8282c5278f1dae7f59bbaa943680d9370cde41b1
```

---

<<<<<<< HEAD
## 📌 Notas
- Sin API key configurada, el sistema funciona en **modo demo** con respuestas predefinidas.
- El historial de conversación se guarda en memoria (se pierde al reiniciar). Para producción, integra Redis o PostgreSQL.
=======
## 📡 Endpoints principales

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| POST | `/auth/login` | Iniciar sesión | ❌ |
| POST | `/auth/register` | Crear cuenta | ❌ |
| POST | `/auth/logout` | Cerrar sesión | ✅ |
| POST | `/auth/reset-password` | Restablecer contraseña | ❌ |
| POST | `/ask` | Chat con GPT-4o | ✅ |
| GET | `/tickets` | Listar tickets | ✅ |
| POST | `/tickets` | Crear ticket | ✅ |
| PATCH | `/tickets/<id>/estado` | Actualizar estado | ✅ |
| GET | `/admin/usuarios` | Listar usuarios | 🔒 Admin |
| GET | `/status` | Estado del sistema | ❌ |

---

## 💡 Decisiones técnicas destacadas

### Compatibilidad iOS / WebKit
El mayor reto fue hacer que la interfaz funcionara correctamente en Safari/iOS. WebKit maneja los eventos táctiles y el `overflow` de forma diferente a Chrome. La solución fue migrar de un sidebar tradicional a una **Bottom Navigation Bar**, lo que mejoró la UX en todos los dispositivos Apple sin sacrificar el diseño en desktop.

### Fallback a memoria
Si PostgreSQL no está configurado, el sistema corre en modo memoria. Esto permite desarrollo y demos sin depender de una base de datos activa.

### GPT-4o Vision
Además del chat de texto, el sistema acepta imágenes. El usuario puede adjuntar una captura de pantalla y GPT-4o analiza visualmente el error, devolviendo un diagnóstico detallado.

---

## 🔄 Historial de versiones

### v2.0 — Marzo 2026
- Mayor rendimiento y estabilidad general
- UX iOS completamente rediseñada (Bottom Nav Bar)
- Corrección de bugs detectados en producción
- Feedback de usuarios internos incorporado
- Panel admin con filtros y buscador mejorado
- Reset de contraseña desde el login

### v1.0 — Enero 2026
- Lanzamiento inicial
- Chat con GPT-4o + análisis de imágenes
- Sistema de tickets con PostgreSQL
- Autenticación con roles Admin / Operador

---

## 👨‍💻 Autor

**Edgar** — Desarrollador Full Stack  
🔗 [LinkedIn](https://linkedin.com/in/ing-edgar-rodriguez-743484206/) · 📧 edgar.guevara.ingindustrial@gmail.com · 🐙 [GitHub](https://github.com/edgarrdz132)

---

> *"Integrar IA en procesos internos no reemplaza al equipo de IT — lo potencia."*
>>>>>>> 8282c5278f1dae7f59bbaa943680d9370cde41b1
