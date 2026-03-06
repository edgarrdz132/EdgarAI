# ⚡ Automatización de Gestión de Incidencias TI con IA

![n8n](https://img.shields.io/badge/n8n-Workflow-FF6D5A?style=flat&logo=n8n&logoColor=white)
![OpenAI](https://img.shields.io/badge/GPT--4.1--mini-OpenAI-10A37F?style=flat&logo=openai&logoColor=white)
![Gmail](https://img.shields.io/badge/Gmail-Notificaciones-EA4335?style=flat&logo=gmail&logoColor=white)
![Status](https://img.shields.io/badge/Status-En%20producción-00d68f?style=flat)

> Sistema de automatización no-code/low-code que clasifica y prioriza incidentes de soporte IT de forma automática usando Inteligencia Artificial — sin intervención humana en el proceso de triaje.

---

## 🧠 ¿Qué problema resuelve?

En entornos de soporte IT sin plataforma ITSM corporativa, los tickets llegan sin clasificar, sin prioridad y sin nivel de escalamiento definido. Esto genera demoras, asignaciones incorrectas y pérdida de trazabilidad.

Este sistema automatiza el proceso completo de **recepción → clasificación → notificación** usando GPT-4.1-mini como motor de inteligencia.

---

## ✨ ¿Cómo funciona?

```
Usuario reporta incidente
        ↓
Webhook recibe los datos (nombre, departamento, descripción)
        ↓
Agente IA (GPT-4.1-mini) clasifica el incidente
        ↓
Structured Output Parser valida el JSON de salida
        ↓
Se genera folio automático (INC + fecha)
        ↓
Notificación por correo al equipo de soporte
```

---

## 🔍 Clasificación automática

El agente de IA clasifica cada incidente en:

| Campo | Opciones |
|---|---|
| **Categoría** | Software · Hardware · Administración · Redes · Otros |
| **Subcategoría** | 40+ subcategorías según la categoría |
| **Prioridad** | Urgente · Alta · Media · Baja |
| **Nivel** | Nivel 1 · Nivel 2 |
| **Folio** | INC + fecha automática (ej. INC20260305) |

---

## 🛠️ Stack Tecnológico

```
Automatización  →  n8n (workflow no-code/low-code)
IA              →  OpenAI GPT-4.1-mini (clasificación y análisis)
Parser          →  Structured Output Parser (JSON validado)
Notificaciones  →  Gmail API (correo automático al equipo)
Trigger         →  Webhook HTTP (recepción de incidentes)
```

---

## 🏗️ Arquitectura del Workflow

```
┌─────────────────────────────────────────────────────┐
│                    ENTRADA                          │
│         Webhook HTTP — recibe el incidente          │
│   { nombre, departamento, descripcion, categoria }  │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│              PROCESAMIENTO — n8n                    │
│                                                     │
│  Edit Fields     →  Mapear campos del webhook       │
│  AI Agent        →  GPT-4.1-mini clasifica          │
│  Output Parser   →  Valida JSON estructurado        │
│  Edit Fields 2   →  Genera folio INC + fecha        │
└───────────┬─────────────────────────────────────────┘
            │
┌───────────▼──────────────────────────────────────┐
│              SALIDA — Gmail                      │
│  Correo automático con:                          │
│  - Folio del ticket                              │
│  - Datos del usuario                             │
│  - Clasificación de la IA                        │
│  - Prioridad y nivel de escalamiento             │
└──────────────────────────────────────────────────┘
```

---

## 📋 Datos de entrada (Webhook)

```json
{
  "nombre y apellido": "Juan Pérez",
  "departamento": "Contabilidad",
  "categoria": "Hardware",
  "subcategoria": "Equipo no enciende",
  "prioridad": "Alta",
  "nivel": "Nivel 2",
  "resumen": "Equipo no enciende",
  "descripcion": "El equipo de cómputo no enciende desde esta mañana.",
  "accion": "Verificar alimentación, cable de poder y encendido"
}
```

---

## 📤 Notificación generada

```
Nuevo Ticket de Soporte TI

Folio del Ticket: INC20260305

DATOS DEL USUARIO:
Reportado por: Juan Pérez
Departamento: Contabilidad
Descripción original: El equipo de cómputo no enciende desde esta mañana.

ANÁLISIS DE LA IA:
Categoría: Hardware
Prioridad: Alta
Nivel de Soporte: Nivel 2
```

---

## 🚀 Cómo usar este workflow

### 1. Requisitos
- n8n instalado (local o en la nube)
- Cuenta de OpenAI con API Key
- Cuenta de Gmail con OAuth2 configurado

### 2. Importar el workflow
```
1. Abrir n8n
2. Ir a Workflows → Import
3. Seleccionar el archivo My_workflow_9.json
4. Configurar las credenciales de OpenAI y Gmail
```

### 3. Configurar credenciales
```
OpenAI:  Configuración → Credenciales → OpenAI API → ingresar API Key
Gmail:   Configuración → Credenciales → Gmail OAuth2 → autorizar cuenta
```

### 4. Activar el workflow
```
Activar el toggle en la esquina superior derecha
Copiar la URL del webhook generada
Usar esa URL como endpoint para recibir tickets
```

---

## 💡 Decisiones técnicas destacadas

### Agente IA con instrucciones estrictas
El system prompt del agente fue diseñado para que la IA **no haga preguntas, no explique decisiones y no invente información** — solo clasifica. Esto garantiza respuestas consistentes y procesables automáticamente.

### Structured Output Parser
Usar el parser estructurado de n8n garantiza que la respuesta de GPT-4.1-mini siempre llegue en JSON válido, evitando errores en los nodos siguientes.

### Folio automático
El folio se genera con la fórmula `INC + fecha actual` — sin base de datos, sin dependencias externas. Simple y funcional.

### Retry automático
El agente tiene configurado `maxTries: 4` — si la IA falla en una clasificación, reintenta automáticamente hasta 4 veces antes de marcar error.

---

## 🔄 Contexto de implementación

Este workflow fue implementado en **Eventos Pabellón M.** como solución ante la ausencia de una plataforma ITSM corporativa. Reemplazó el proceso manual de recepción y clasificación de tickets, mejorando la trazabilidad y reduciendo los tiempos de asignación al equipo de soporte.

---

## 👨‍💻 Autor

**Edgar Misael Guevara Rodriguez** — IT Engineer & AI Developer
🔗 [LinkedIn](https://linkedin.com/in/ing-edgar-rodriguez-743484206/) · 📧 edgar.guevara.ingindustrial@gmail.com · 🤖 [EdgarAI](https://github.com/edgarrdz132/edgarai)

---

> *"Cuando no tienes las herramientas, las construyes."*
