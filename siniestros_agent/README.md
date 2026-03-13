# Siniestros AMV Agent - "Berta" (CAS Expert)

Agente de IA para la gestión automatizada de siniestros sanitarios del **Convenio de Asistencia Sanitaria (CAS)** usando **Google Agent Development Kit (ADK)** y **Gemini 2.5 Flash**.

## 🚀 Ejecución Rápida

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Autenticación GCP
gcloud auth application-default login

# 3. Ejecutar el agente
adk web
```

Abrir `http://localhost:8000` en el navegador.

## 🏗️ Arquitectura

```
siniestros_agent/
├── agent.py              # Agente ADK nativo (root_agent)
├── prompts.py            # System prompt con flujo CAS completo
├── tools.py              # 13 herramientas de validación + SIAX
├── cas_codes.py          # Máquina de estados códigos CAS
├── mock_data.py          # BBDD simulada (pólizas, hospitales, etc.)
├── siax_client.py        # Cliente REST para ServiciosGemini (SIAX)
├── knowledge_loader.py   # Extracción de texto de PDFs/DOCX
├── api_server.py         # Servidor FastAPI con endpoints CAS + SIAX
├── schemas.py            # Modelos Pydantic para API
├── queue_manager.py      # Cola de validación humana (SQLite)
├── simulation_test.py    # Tests unitarios + integración
├── requirements.txt      # Dependencias
├── .env                  # Configuración (credenciales SIAX, GCP)
├── .documentation/       # Manuales CAS normativos + casos de prueba
```

## 🔧 Herramientas del Agente (13)

| Herramienta | Función |
|------------|---------|
| `verify_injured_person` | Verifica lesionado por DNI/matrícula |
| `verify_insurance_policy` | Verifica póliza vigente en fecha accidente |
| `verify_accident` | Comprueba existencia y datos del siniestro |
| `check_cas_code_sequence` | Valida secuencia de códigos CAS |
| `check_hospital_adhesion` | Verifica adhesión hospital al convenio |
| `check_tariffs` | Valida importes contra baremos CAS |
| `read_attached_document` | Lee PDFs/imágenes adjuntos |
| `verify_injury_consistency` | Cruza lesión vs dinámica accidente |
| `search_case_history` | Busca historial de expediente |
| `validate_cas_dates` | Valida coherencia temporal |
| `generate_cas_response_code` | Genera respuesta CAS formal |
| `analizar_caso_siax` | 🔗 **Botón 1**: Analiza caso completo desde SIAX |
| `analizar_mensaje_siax` | 🔗 **Botón 2**: Recomienda respuesta a mensaje SIAX |

## 🔗 Integración SIAX (ServiciosGemini)

Berta se conecta en tiempo real al servicio SIAX para consultar datos de reclamaciones CAS:

| Endpoint API | Descripción |
|-------------|-------------|
| `GET /cas/siax/test` | Verificar conexión con SIAX |
| `POST /cas/siax/analizar-caso` | Analizar todas las conversaciones de un caso |
| `POST /cas/siax/analizar-mensaje` | Recomendar respuesta a un mensaje específico |

```bash
# Probar conexión SIAX
curl http://localhost:8080/cas/siax/test

# Analizar caso completo (Botón 1)
curl -X POST http://localhost:8080/cas/siax/analizar-caso \
  -H "Content-Type: application/json" -d '{"id_cas": 15}'

# Recomendar respuesta (Botón 2)
curl -X POST http://localhost:8080/cas/siax/analizar-mensaje \
  -H "Content-Type: application/json" -d '{"id_cas": 15, "id_mensaje": 50}'
```

## 🧪 Tests

```bash
# Ejecutar todos los tests
python -m pytest simulation_test.py -v -s

# O con el runner incluido
python run_tests.py
```

## 📋 Ejemplo de Uso

En la interfaz ADK web, enviar un mensaje como:

> "He recibido un parte de asistencia inicial (código 100) del Hospital General Universitario (HOSP_001) para el lesionado Juan García López (DNI: 12345678A, matrícula 1234ABC). Siniestro SIN-2024-001, colisión trasera el 15/11/2024. Lesión: Cervicalgia."

O para usar SIAX:

> "Analiza el caso CAS con id 15 desde SIAX y dime a cuáles puedo responder."

> "Del caso CAS 15, analiza el mensaje con id 50 y recomiéndame qué código de respuesta enviar."

## ⚙️ Configuración

| Variable | Default | Descripción |
|----------|---------|-------------|
| `CAS_MODEL` | `gemini-2.5-flash` | Modelo de IA |
| `GOOGLE_CLOUD_PROJECT` | `pmo-piloto-gemini-enterprise` | Proyecto GCP |
| `GOOGLE_CLOUD_LOCATION` | `europe-west1` | Región GCP |
| `SIAX_USERNAME` | — | Usuario SIAX |
| `SIAX_PASSWORD` | — | Contraseña SIAX |
| `SIAX_URL` | `https://desarrollo.senassur.com/...` | URL del servicio |
| `SIAX_ENVIRONMENT` | `test` | Entorno: `test` o `produccion` |
