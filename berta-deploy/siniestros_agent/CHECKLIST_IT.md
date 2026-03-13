# 📋 Checklist IT — Integración con Berta CAS

> **Objetivo:** Conectar el sistema actual al agente Berta para automatizar el análisis de partes CAS.  
> Una vez completados estos puntos, el equipo de IA realizará los cambios finales para activar la integración.

---

## ✅ Lo que necesita hacer IT

### 1. Exponer los datos del parte CAS

Cuando el sistema reciba un mensaje de un hospital, debe ser capaz de extraer y enviar estos campos:

| Campo | Obligatorio | Ejemplo |
|-------|:-----------:|---------|
| `expediente_id` | ✅ | `"202600086262"` |
| `codigo_cas` | ✅ | `"100"` |
| `hospital_id` | ✅ | `"HOSP_001"` |
| `fecha_ocurrencia` | Recomendado | `"2025-11-15"` |
| `matricula_asegurado` | Recomendado | `"1234ABC"` |
| `lesionado_dni` | Recomendado | `"12345678A"` |
| `lesionado_nombre` | Opcional | `"Juan García López"` |
| `lesion_declarada` | Recomendado | `"Cervicalgia postraumática"` |
| `tipo_accidente` | Opcional | `"Colisión trasera"` |
| `importe_reclamado` | Solo cód. 500 | `1250.00` |
| `documentos` (array) | Opcional | `[{"nombre_archivo": "doc.pdf"}]` |

---

### 2. Hacer una llamada HTTP cuando llegue un parte

Al recibir un parte CAS, hacer un **POST** a Berta:

```http
POST http://<servidor-berta>:8080/cas/parte
Content-Type: application/json

{
  "expediente_id": "202600086262",
  "codigo_cas": "100",
  "hospital_id": "HOSP_001",
  "fecha_ocurrencia": "2025-11-15",
  "matricula_asegurado": "1234ABC",
  "lesionado_dni": "12345678A",
  "lesion_declarada": "Cervicalgia postraumática"
}
```

La llamada devuelve en ~15-30 segundos la respuesta de Berta.

---

### 3. Mostrar la propuesta al tramitador

Con la respuesta recibida, mostrar en la pantalla del tramitador:

| Campo de la respuesta | Qué mostrar |
|-----------------------|-------------|
| `estado_cola` | Semáforo: 🟢 Auto / 🟡 Revisar / 🔴 Intervención |
| `decision` | `ACEPTAR` / `SOLICITAR_DOCUMENTACION` / `REHUSAR` |
| `confianza` | `ALTA` / `MEDIA` / `BAJA` |
| `justificacion_normativa` | Texto del razonamiento de Berta |
| `nota_expediente` | Texto listo para pegar en el expediente |
| `alertas` | Lista de avisos (posible fraude, datos inconsistentes...) |

---

### 4. Guardar el `id_analisis`

La respuesta incluye un `id_analisis` (UUID). **Guardarlo vinculado al expediente.** Se necesitará en el paso 5.

```json
{ "id_analisis": "a1b2c3d4-e5f6-..." }
```

---

### 5. Notificar cuando el tramitador valide

Cuando el tramitador pulse **Aceptar / Rechazar** en su pantalla, hacer:

```http
PATCH http://<servidor-berta>:8080/cas/cola/{id_analisis}/validar
Content-Type: application/json

{
  "validacion": "APROBADO",
  "tramitador_id": "nombre.apellido"
}
```

Valores posibles de `validacion`:
- `APROBADO` → tramitador acepta la decisión de Berta
- `RECHAZADO` → tramitador toma otra decisión
- `MODIFICADO` → acepta con cambios (añadir `"codigo_cas_final": "300"`)

---

### 6. Usar el `codigo_cas_respuesta` para emitir al hospital

Una vez validado, el sistema IT emite la respuesta al hospital usando el código CAS de la respuesta:

```json
{ "codigo_cas_respuesta": "200" }
```

---

## ❌ Lo que NO necesita hacer IT

- No gestionar modelos de IA
- No entender la lógica de los códigos CAS
- No cambiar su base de datos actual
- No gestionar documentos (Berta los lee si se pasan los nombres)

---

## 🔌 Información de conexión (a proporcionar por el equipo de IA)

| Dato | Valor (pendiente de confirmar) |
|------|-------------------------------|
| URL base | `http://<servidor>:8080` |
| Autenticación | API Key en header `X-API-Key` |
| Timeout recomendado | 60 segundos |
| Docs interactivos | `http://<servidor>:8080/docs` |

---

## 📬 Cuando esté listo

Avisar al equipo de IA con:
1. **URL de su webhook/endpoint** donde Berta debe notificar si hay cambios de estado
2. **Formato de sus IDs internos** de expediente (para mapeo)
3. **ID de hospital** que usáis internamente (para mapear a los IDs de Berta)
4. **Entorno de pruebas** disponible para hacer las primeras pruebas de integración

