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
```

---

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
```bash
python app.py
```

### 6. Abrir en el navegador
```
http://localhost:5000
```

---

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
```

---

## 📌 Notas
- Sin API key configurada, el sistema funciona en **modo demo** con respuestas predefinidas.
- El historial de conversación se guarda en memoria (se pierde al reiniciar). Para producción, integra Redis o PostgreSQL.
