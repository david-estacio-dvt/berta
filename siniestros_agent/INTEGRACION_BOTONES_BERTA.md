# Integración Berta CAS — Guía para Equipo IT

## URL del Servicio

```
https://berta-cas-6uvwmst6tq-ew.a.run.app
```

Swagger UI (documentación interactiva):  
https://berta-cas-6uvwmst6tq-ew.a.run.app/docs

---

## Botón 1 — "Analizar caso"

Analiza todas las secuencias del caso y devuelve cuáles necesitan respuesta.

**Cuándo llamar**: Cuando el tramitador abre la ventana de conversaciones de un caso CAS.  
**Qué hacer con la respuesta**: Los mensajes con `necesita_accion: true` → marcar en **negrita**.

### Request

```
POST https://berta-cas-6uvwmst6tq-ew.a.run.app/cas/siax/analizar-caso
Content-Type: application/json

{
  "id_cas": 15
}
```

### Response (ejemplo)

```json
{
  "id_cas": 15,
  "total_secuencias": 3,
  "secuencias_respondibles": 2,
  "analisis_berta": "He analizado el caso con 3 secuencias...",
  "secuencias": [
    {
      "referencia_cas": "202400472741",
      "necesita_accion": false,
      "ultimo_codigo": "483",
      "mensajes": [...]
    },
    {
      "referencia_cas": "202400612914",
      "necesita_accion": true,
      "ultimo_codigo": "175",
      "codigos_respuesta_disponibles": ["200", "300", "301", "475", "900"],
      "mensajes": [
        {
          "id": 3258,
          "codigo": "175",
          "estado": "Recibido",
          "emisor": "HOSPITAL",
          "caducado": false,
          "puede_responder": true
        }
      ]
    }
  ]
}
```

**Campos clave para el frontend:**
- `secuencias[].necesita_accion` → `true` = marcar en negrita
- `secuencias[].codigos_respuesta_disponibles` → los códigos posibles de respuesta
- `analisis_berta` → texto del análisis de la IA

---

## Botón 2 — "Recomendar respuesta"

Dado un mensaje específico, Berta recomienda qué código CAS enviar con justificación normativa.

**Cuándo llamar**: Cuando el tramitador pincha un mensaje marcado en negrita y ve los códigos de respuesta.  
**Qué hacer con la respuesta**: Resaltar el código recomendado y mostrar la justificación.

### Request

```
POST https://berta-cas-6uvwmst6tq-ew.a.run.app/cas/siax/analizar-mensaje
Content-Type: application/json

{
  "id_cas": 15,
  "id_mensaje": 3258
}
```

### Response (ejemplo)

```json
{
  "id_cas": 15,
  "id_mensaje": 3258,
  "codigo_mensaje": "175",
  "recomendacion_berta": {
    "codigo_respuesta": "200",
    "decision": "ACEPTAR",
    "confianza": "ALTA",
    "justificacion": "Según normas V43, art. 4.2, el parte 175 con documentación completa y lesión coherente procede aceptar...",
    "alternativas": [
      {"codigo": "301", "motivo": "Solo si falta documentación"},
      {"codigo": "900", "motivo": "Solo si hay motivo de rehúse"}
    ]
  }
}
```

**Campos clave para el frontend:**
- `recomendacion_berta.codigo_respuesta` → el código a resaltar en verde
- `recomendacion_berta.justificacion` → mostrar debajo como texto explicativo
- `recomendacion_berta.confianza` → ALTA / MEDIA / BAJA

---

## Verificación rápida

Para verificar que el servicio funciona:

```
GET https://berta-cas-6uvwmst6tq-ew.a.run.app/health
→ {"status": "ok", "agente": "berta_cas_agent"}

GET https://berta-cas-6uvwmst6tq-ew.a.run.app/cas/siax/test
→ {"ok": true, "environment": "test", "status_code": 200}
```

---

## Notas

- **Timeout recomendado**: 120 segundos (la primera llamada tras inactividad tarda más por cold start)
- **Formato**: Todas las llamadas son JSON sobre HTTPS
- **Autenticación**: No requiere api-key por ahora (se activará antes de producción)
- **Disponibilidad**: 24/7, desplegado en Google Cloud Run (europe-west1)
- **id_cas para pruebas**: usar `15` (tiene 3 secuencias y 12 mensajes reales)
