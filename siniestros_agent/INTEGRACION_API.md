# 🤖 Guía de Integración API — Berta CAS

**Versión:** 1.0  
**Agente:** Berta — Tramitadora Experta CAS (AMV Siniestros)  
**Contacto técnico:** Equipo de IA AMV

---

## ¿Qué hace esta API?

La API de Berta recibe automáticamente los partes CAS que llegan de los hospitales, los analiza usando IA y devuelve una **decisión justificada** que queda en una **cola de validación humana** para que el tramitador la revise antes de emitir la respuesta definitiva al hospital.

```
Hospital  →  Sistema IT  →  POST /cas/parte  →  Berta (IA)  →  Cola SQLite  →  Tramitador
                                                                               ↓
                                                                    PATCH /cas/cola/{id}/validar
                                                                               ↓
                                                               Sistema IT emite respuesta CAS
```

---

## 🚀 Arranque del Servidor

### 1. Instalar dependencias

```bash
cd C:\Users\destacio\.gemini\antigravity\scratch\siniestros_agent
pip install -r requirements.txt
```

### 2. Configurar credenciales (`.env`)

```env
GOOGLE_CLOUD_PROJECT=pmo-piloto-gemini-enterprise
GOOGLE_CLOUD_LOCATION=europe-west1
GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

### 3. Arrancar el servidor

```bash
# Desde el directorio raíz (scratch/):
uvicorn siniestros_agent.api_server:app --host 0.0.0.0 --port 8080 --reload
```

#### Docker (producción)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY siniestros_agent/ ./siniestros_agent/
RUN pip install -r siniestros_agent/requirements.txt
EXPOSE 8080
CMD ["uvicorn", "siniestros_agent.api_server:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 4. Verificar que funciona

```bash
curl http://localhost:8080/health
# {"status":"ok","agente":"berta_cas_agent","timestamp":"2026-02-24T..."}
```

**Documentación interactiva (Swagger):** `http://localhost:8080/docs`

---

## 📡 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/cas/parte` | ⭐ **Enviar parte CAS a Berta** |
| `GET` | `/cas/cola` | Listar cola de validación |
| `GET` | `/cas/cola/{id}` | Detalle completo de un análisis |
| `PATCH` | `/cas/cola/{id}/validar` | El tramitador valida/rechaza la propuesta |
| `GET` | `/cas/siax/test` | 🔗 Verificar conexión con SIAX |
| `POST` | `/cas/siax/analizar-caso` | 🔗 **Botón 1: Analizar todas las conversaciones** |
| `POST` | `/cas/siax/analizar-mensaje` | 🔗 **Botón 2: Recomendar respuesta a un mensaje** |

---

## 📥 POST `/cas/parte` — Enviar un parte CAS

### Request Body

```json
{
  "expediente_id": "202600086262",
  "codigo_cas": "100",
  "convenio_tipo": "PUBLICO",
  "hospital_id": "HOSP_001",
  "hospital_nombre": "Hospital General Universitario",
  "siniestro_id": "SIN-2024-001",
  "fecha_ocurrencia": "2025-11-15",
  "tipo_accidente": "Colisión trasera en vía urbana",
  "matricula_asegurado": "1234ABC",
  "matricula_contrario": "XXXX999",
  "lesionado_nombre": "Juan García López",
  "lesionado_dni": "12345678A",
  "lesionado_posicion": "Conductor",
  "lesion_declarada": "Cervicalgia postraumática",
  "documentos": [
    {
      "nombre_archivo": "202600086262-107636405-001.PDF",
      "tipo": "pdf",
      "descripcion": "Informe urgencias"
    }
  ]
}
```

### Campos obligatorios

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `expediente_id` | string | ID del expediente CAS |
| `codigo_cas` | string | Código CAS recibido: `"100"`, `"328"`, `"500"`... |
| `hospital_id` | string | ID del hospital en el sistema |

### Campos opcionales pero recomendados

| Campo | Descripción |
|-------|-------------|
| `fecha_ocurrencia` | Fecha del accidente (YYYY-MM-DD) |
| `matricula_asegurado` | Matrícula del vehículo asegurado |
| `lesionado_dni` | DNI del lesionado — clave para verificación |
| `lesion_declarada` | Descripción de la lesión |
| `documentos` | Lista de documentos adjuntos del hospital |

### Campos de facturación (solo código 500/501)

| Campo | Descripción |
|-------|-------------|
| `importe_reclamado` | Total en euros |
| `servicios_facturados` | Array de servicios: `[{codigo, descripcion, cantidad, precio_unitario}]` |

---

## 📤 Response — BertaResponse

```json
{
  "expediente_id": "202600086262",
  "codigo_cas_recibido": "100",
  "timestamp_analisis": "2026-02-24T13:25:00Z",
  "id_analisis": "a1b2c3d4-...",
  "decision": "ACEPTAR",
  "codigo_cas_respuesta": "200",
  "confianza": "ALTA",
  "estado_cola": "PENDIENTE_VALIDACION",
  "requiere_accion_humana": true,
  "resumen_caso": "Hospital HOSP_001 envía parte 100. Lesionado: Juan García...",
  "verificaciones": [
    {"nombre": "✅ Póliza vigente", "resultado": "OK", "detalle": "Póliza activa en fecha 2025-11-15"},
    {"nombre": "✅ Hospital adherido", "resultado": "OK", "detalle": "HOSP_001 en convenio PUBLICO"},
    {"nombre": "⚠️ Fecha reciente", "resultado": "ALERTA", "detalle": "Parte recibido a 5 días del siniestro"}
  ],
  "justificacion_normativa": "La póliza 1234ABC estaba vigente en fecha de ocurrencia...",
  "alertas": ["Verificar telefónicamente identidad del lesionado"],
  "nota_expediente": "24/02/2026 13:25 - PROPUESTA ACEPTAR (cod.200) - Analizado por Berta (IA CAS) - Pendiente de validación humana",
  "respuesta_completa": "## 📋 Resumen del Caso\n..."
}
```

### Estados de cola (`estado_cola`)

| Valor | Icono | Significado | Acción requerida |
|-------|-------|-------------|-----------------|
| `PROCESADO_AUTOMATICAMENTE` | 🟢 | Confianza ALTA, todo OK | Se puede ejecutar sin revisión |
| `PENDIENTE_VALIDACION` | 🟡 | Confianza MEDIA o hay alertas | El tramitador debe revisar |
| `REQUIERE_INTERVENCION_MANUAL` | 🔴 | Confianza BAJA o posible fraude | Revisión obligatoria |

### Decisiones (`decision`)

| Valor | Código CAS | Descripción |
|-------|-----------|-------------|
| `ACEPTAR` | 200 | Acepta el parte |
| `ACEPTAR_CON_RESERVAS` | 300 | Acepta con condiciones |
| `SOLICITAR_DOCUMENTACION` | 301 | Pide más documentación al hospital |
| `REHUSAR` | 900 | Rechaza el parte |
| `PENDIENTE_INFO` | — | Berta necesita más datos |

---

## 📋 GET `/cas/cola` — Listar cola

```bash
# Todos los pendientes
curl http://localhost:8080/cas/cola?estado=PENDIENTE

# Todos sin filtro
curl http://localhost:8080/cas/cola
```

```json
[
  {
    "id_analisis": "a1b2c3d4-...",
    "expediente_id": "202600086262",
    "codigo_cas": "100",
    "decision_berta": "ACEPTAR",
    "confianza": "ALTA",
    "estado_cola": "PENDIENTE_VALIDACION",
    "estado_validacion": "PENDIENTE",
    "timestamp_analisis": "2026-02-24T13:25:00Z"
  }
]
```

---

## ✅ PATCH `/cas/cola/{id_analisis}/validar` — Validar propuesta

El tramitador revisa la propuesta de Berta y emite su decisión:

```bash
curl -X PATCH http://localhost:8080/cas/cola/a1b2c3d4-.../validar \
  -H "Content-Type: application/json" \
  -d '{
    "validacion": "APROBADO",
    "tramitador_id": "david.estacio",
    "notas_tramitador": "Conforme con la decisión de Berta. Emitido código 200."
  }'
```

| Campo `validacion` | Significado |
|--------------------|-------------|
| `APROBADO` | El tramitador acepta la propuesta de Berta |
| `RECHAZADO` | El tramitador toma una decisión diferente |
| `MODIFICADO` | Acepta con cambios (enviar `codigo_cas_final`) |

---

## 🔐 Autenticación

La API acepta dos métodos de autenticación:

### Opción A — API Key en header (recomendada para M2M)
```
X-API-Key: <tu-api-key>
```

### Opción B — Bearer token (si ya tenéis OAuth2 en el sistema IT)
```
Authorization: Bearer <token>
```

> ⚠️ **La autenticación no está activa por defecto** en esta versión. Para activarla, añadir en `api_server.py` el middleware de seguridad correspondiente y configurar las claves en el `.env`.

---

## 🔄 Flujo completo de integración

```
1. Hospital envía mensaje CAS al sistema IT
         ↓
2. Sistema IT hace POST /cas/parte con los datos del parte
         ↓
3. Berta analiza (~10-30 segundos): verifica póliza, siniestro,
   hospital, coherencia lesión, documentos...
         ↓
4. Berta devuelve BertaResponse con:
   - decision: ACEPTAR / SOLICITAR_DOC / REHUSAR
   - estado_cola: 🟢/🟡/🔴
   - justificacion_normativa
   - nota_expediente (lista para copiar al expediente)
         ↓
5. El análisis queda en SQLite (berta_cola.sqlite)
         ↓
6. El tramitador revisa la cola (GET /cas/cola)
         ↓
7. El tramitador valida (PATCH /cas/cola/{id}/validar)
         ↓
8. El sistema IT emite la respuesta CAS al hospital
   usando el codigo_cas_respuesta aprobado
```

---

## 🗄️ Base de datos (Cola SQLite)

La cola se almacena en `siniestros_agent/berta_cola.sqlite`.

Para producción, se recomienda migrar a **PostgreSQL** cambiando la función `_get_conn()` en `queue_manager.py` para usar `psycopg2` o `asyncpg`.

### Tabla `cola_validacion`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id_analisis` | TEXT PK | UUID único del análisis |
| `expediente_id` | TEXT | ID del expediente CAS |
| `codigo_cas` | TEXT | Código CAS recibido |
| `decision_berta` | TEXT | Decisión de Berta |
| `confianza` | TEXT | ALTA / MEDIA / BAJA |
| `estado_cola` | TEXT | Estado de la cola |
| `estado_validacion` | TEXT | PENDIENTE / APROBADO / RECHAZADO |
| `timestamp_analisis` | TEXT | Cuándo analizó Berta |
| `timestamp_validacion` | TEXT | Cuándo validó el tramitador |
| `tramitador_id` | TEXT | ID del tramitador |
| `payload_completo` | TEXT | JSON completo de BertaResponse |

---

## ⚙️ Variables de entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `GOOGLE_CLOUD_PROJECT` | ID proyecto GCP | `pmo-piloto-gemini-enterprise` |
| `GOOGLE_CLOUD_LOCATION` | Región Vertex AI | `europe-west1` |
| `GOOGLE_GENAI_USE_VERTEXAI` | Usar Vertex AI (no Gemini API) | `TRUE` |
| `CAS_MODEL` | Modelo a usar (opcional) | `gemini-2.5-flash` |
| `API_KEY` | Clave de API (si se activa auth) | `sk-...` |

---

## 📊 Códigos de error HTTP

| Código | Significado |
|--------|-------------|
| `200` | OK |
| `404` | Análisis no encontrado en la cola |
| `422` | Error de validación en el payload (campo requerido falta o tiene formato incorrecto) |
| `502` | Error al conectar con el agente Berta (Vertex AI / modelo no disponible) |

---

## 🧪 Ejemplo de prueba con curl

```bash
# Caso de aceptación
curl -X POST http://localhost:8080/cas/parte \
  -H "Content-Type: application/json" \
  -d '{
    "expediente_id": "202600086262",
    "codigo_cas": "100",
    "hospital_id": "HOSP_001",
    "fecha_ocurrencia": "2025-11-15",
    "matricula_asegurado": "1234ABC",
    "lesionado_dni": "12345678A",
    "lesionado_nombre": "Juan García López",
    "lesionado_posicion": "Conductor",
    "lesion_declarada": "Cervicalgia postraumática",
    "tipo_accidente": "Colisión trasera"
  }'
```

```bash
# Ver cola pendiente
curl http://localhost:8080/cas/cola?estado=PENDIENTE

# Ver detalle completo del análisis
curl http://localhost:8080/cas/cola/a1b2c3d4-.../

# Validar como aprobado
curl -X PATCH http://localhost:8080/cas/cola/a1b2c3d4-.../validar \
  -H "Content-Type: application/json" \
  -d '{"validacion":"APROBADO","tramitador_id":"david.estacio"}'
```

---

## � SIAX / ServiciosGemini — Endpoints

### GET `/cas/siax/test` — Verificar conexión

```bash
curl http://localhost:8080/cas/siax/test
# {"ok":true,"mensaje":"El servicio funciona correctamente","environment":"test"}
```

### POST `/cas/siax/analizar-caso` — Botón 1: Analizar caso completo

Obtiene todas las secuencias y mensajes de un caso CAS desde SIAX, y Berta analiza cuáles requieren respuesta.

```bash
curl -X POST http://localhost:8080/cas/siax/analizar-caso \
  -H "Content-Type: application/json" \
  -d '{"id_cas": 15}'
```

**Response:**
```json
{
  "id_cas": 15,
  "total_secuencias": 3,
  "total_mensajes": 12,
  "secuencias_respondibles": 2,
  "secuencias": [
    {
      "referencia_cas": "202400472741",
      "total_mensajes": 3,
      "ultimo_codigo": "483",
      "necesita_accion": false,
      "mensajes": [...]
    }
  ],
  "analisis_berta": "## 📋 Resumen del Caso\n...(análisis completo de Berta)...",
  "timestamp": "2026-02-28T..."
}
```

### POST `/cas/siax/analizar-mensaje` — Botón 2: Recomendar respuesta

Analiza un mensaje específico y Berta recomienda con qué código CAS responder.

```bash
curl -X POST http://localhost:8080/cas/siax/analizar-mensaje \
  -H "Content-Type: application/json" \
  -d '{"id_cas": 15, "id_mensaje": 50}'
```

**Response:**
```json
{
  "id_cas": 15,
  "id_mensaje": 50,
  "referencia_cas": "202400472741",
  "mensaje": {
    "id": 50,
    "codigo": "171",
    "emisor": "HOSPITAL",
    "estado": "Recibido",
    "convenio_normas": "10199",
    "puede_responder": true,
    "codigos_respuesta_validos": ["200", "300", "301", "900", "999"]
  },
  "historial_secuencia": [...],
  "analisis_berta": "## 🎯 Recomendación\n...(código recomendado + justificación)...",
  "timestamp": "2026-02-28T..."
}
```

### Configuración SIAX (`.env`)

```env
SIAX_USERNAME=GeminiUsr#25
SIAX_PASSWORD=GeminiP4ss#25
SIAX_URL=https://desarrollo.senassur.com/ServiciosGemini.svc/rest
SIAX_ENVIRONMENT=test
```

Para producción:
```env
SIAX_URL=https://www.senassur.com:8086/Xena/ServiciosGemini.svc/rest
SIAX_ENVIRONMENT=produccion
```

---

## �📞 Soporte

Para cualquier duda técnica sobre la integración, contactar con el equipo de IA AMV.

La documentación interactiva completa (Swagger UI) está disponible en:
**`http://<servidor>:8080/docs`**
