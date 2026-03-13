"""
api_server.py - Servidor REST de Berta CAS para integración con el sistema de IT.

Expone la funcionalidad del agente Berta como una API HTTP.
El sistema de IT envía los partes CAS y recibe respuestas estructuradas.
Las respuestas quedan encoladas para validación humana.

Arrancar con:
    uvicorn api_server:app --host 0.0.0.0 --port 8080 --reload
"""

import os
import sys
import re
import uuid
import asyncio
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

# Añadir directorio actual al path para imports
sys.path.insert(0, os.path.dirname(__file__))

# Cargar variables de entorno desde .env
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from schemas import (
    ParteInput, BertaResponse, ValidacionHumana, ItemCola,
    EstadoCola, NivelConfianza, DecisionBerta, EstadoValidacion,
    VerificacionDetalle,
    SiaxAnalisisCasoRequest, SiaxAnalisisMensajeRequest, SiaxAnalisisResponse,
)
from queue_manager import init_db, encolar_analisis, obtener_cola, obtener_analisis, validar_analisis, nueva_id
import siax_client

# ─────────────────────────────────────────────
# Setup ADK
# ─────────────────────────────────────────────

from google.adk.runners import InMemoryRunner
from siniestros_agent.agent import root_agent
from google.genai.types import Content, Part

# ─────────────────────────────────────────────
# FastAPI App
# ─────────────────────────────────────────────

app = FastAPI(
    title="Berta CAS API",
    description="API REST para el agente tramitador de siniestros CAS. Recibe partes de asistencia sanitaria y devuelve decisiones justificadas encoladas para validación humana.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    init_db()
    print("✅ Berta CAS API iniciada. Cola de validación lista.")


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def _build_prompt(parte: ParteInput) -> str:
    """Construye el mensaje de texto para enviar a Berta a partir del ParteInput."""
    docs_str = ""
    if parte.documentos:
        docs_str = "\nDocumentación adjunta:\n"
        for doc in parte.documentos:
            docs_str += f"- {doc.nombre_archivo} ({doc.descripcion or doc.tipo or 'documento'})\n"

    servicios_str = ""
    if parte.importe_reclamado:
        servicios_str = f"\nFacturación:\n- Importe reclamado: {parte.importe_reclamado:.2f} €\n"
        if parte.servicios_facturados:
            for s in parte.servicios_facturados:
                servicios_str += f"  · {s.get('descripcion','?')}: {s.get('cantidad',1)}x {s.get('precio_unitario',0):.2f} €\n"

    prompt = f"""NUEVO MENSAJE CAS RECIBIDO - Expediente: {parte.expediente_id}

📩 Mensaje entrante del sistema CAS:
- Código CAS: {parte.codigo_cas}
- Hospital: {parte.hospital_id}{' (' + parte.hospital_nombre + ')' if parte.hospital_nombre else ''}
- Convenio: {parte.convenio_tipo or 'PUBLICO'}

Datos del Parte:"""

    if parte.fecha_ocurrencia:
        prompt += f"\n- Fecha de ocurrencia del siniestro: {parte.fecha_ocurrencia}"
    if parte.matricula_asegurado:
        prompt += f"\n- Matrícula vehículo asegurado: {parte.matricula_asegurado}"
    if parte.matricula_contrario:
        prompt += f"\n- Segunda matrícula implicada: {parte.matricula_contrario}"
    if parte.lesionado_nombre:
        prompt += f"\n- Lesionado: {parte.lesionado_nombre}"
    if parte.lesionado_dni:
        prompt += f"\n- DNI lesionado: {parte.lesionado_dni}"
    if parte.lesionado_posicion:
        prompt += f"\n- Posición en vehículo: {parte.lesionado_posicion}"
    if parte.tipo_accidente:
        prompt += f"\n- Tipo de accidente: {parte.tipo_accidente}"
    if parte.lesion_declarada:
        prompt += f"\n- Lesión declarada: {parte.lesion_declarada}"
    if parte.siniestro_id:
        prompt += f"\n- Siniestro referencia: {parte.siniestro_id}"
    if parte.notas_hospital:
        prompt += f"\n- Notas del hospital: {parte.notas_hospital}"

    prompt += servicios_str
    prompt += docs_str
    prompt += "\n\nAnaliza este parte y dame tu decisión completa con justificación normativa siguiendo el formato de respuesta estructurado."
    return prompt


def _parse_berta_response(
    texto: str,
    parte: ParteInput,
    id_analisis: str,
) -> BertaResponse:
    """
    Parsea la respuesta en texto de Berta y extrae los campos estructurados.
    Si no puede parsear algún campo, usa valores por defecto conservadores.
    """

    # --- Determinar decisión ---
    texto_upper = texto.upper()
    if "REHUSAR" in texto_upper or "REHÚSO" in texto_upper or "REHÚSE" in texto_upper or "REHÚSA" in texto_upper or "RECHAZ" in texto_upper:
        decision = DecisionBerta.REHUSAR
    elif "SOLICITAR DOCUMENTACIÓN" in texto_upper or "CÓDIGO 362" in texto_upper or "CODIGO 362" in texto_upper:
        decision = DecisionBerta.SOLICITAR_DOC
    elif "ACEPTAR" in texto_upper or "CÓDIGO 271" in texto_upper or "CODIGO 271" in texto_upper:
        decision = DecisionBerta.ACEPTAR
    else:
        decision = DecisionBerta.PENDIENTE

    # --- Determinar código CAS de respuesta ---
    codigo_respuesta = None
    m = re.search(r'\*\*Código CAS\*\*:\s*(\d+)', texto)
    if m:
        codigo_respuesta = m.group(1)
    else:
        decision_to_code = {
            DecisionBerta.ACEPTAR: "271",
            DecisionBerta.SOLICITAR_DOC: "362",
            DecisionBerta.REHUSAR: "471",
        }
        codigo_respuesta = decision_to_code.get(decision)

    # --- Determinar confianza ---
    if "CONFIANZA: ALTA" in texto_upper or "ALTA (>" in texto_upper:
        confianza = NivelConfianza.ALTA
    elif "CONFIANZA: BAJA" in texto_upper or "BAJA (<" in texto_upper:
        confianza = NivelConfianza.BAJA
    else:
        confianza = NivelConfianza.MEDIA

    # --- Determinar estado cola ---
    if "PROCESADO AUTOMÁTICAMENTE" in texto_upper or "🟢" in texto:
        estado_cola = EstadoCola.PROCESADO_AUTO
        requiere_humano = False
    elif "REQUIERE INTERVENCIÓN MANUAL" in texto_upper or "🔴" in texto:
        estado_cola = EstadoCola.REQUIERE_INTERVENCION
        requiere_humano = True
    else:
        estado_cola = EstadoCola.PENDIENTE_VALIDACION
        requiere_humano = True

    # --- Extraer alertas ---
    alertas = []
    alertas_section = re.search(r'## .*Alertas.*\n(.*?)(?=##|\Z)', texto, re.DOTALL | re.IGNORECASE)
    if alertas_section:
        for line in alertas_section.group(1).split('\n'):
            line = line.strip().lstrip('- •*')
            if line and len(line) > 5:
                alertas.append(line)

    # --- Extraer justificación normativa ---
    just_section = re.search(r'## .*Justificaci[oó]n Normativa.*\n(.*?)(?=##|\Z)', texto, re.DOTALL | re.IGNORECASE)
    justificacion = just_section.group(1).strip() if just_section else texto[:500]

    # --- Extraer nota de expediente ---
    nota_section = re.search(r'## .*Nota de Expediente.*\n(.*?)(?=##|\Z)', texto, re.DOTALL | re.IGNORECASE)
    nota = nota_section.group(1).strip() if nota_section else f"Analizado por Berta (IA CAS) - {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC - Pendiente de validación humana"

    # --- Extraer resumen ---
    res_section = re.search(r'## .*Resumen.*\n(.*?)(?=##|\Z)', texto, re.DOTALL | re.IGNORECASE)
    resumen = res_section.group(1).strip()[:500] if res_section else f"Expediente {parte.expediente_id} | Código {parte.codigo_cas} | {parte.hospital_id}"

    # --- Verificaciones (simplificado) ---
    verificaciones = []
    ver_section = re.search(r'## .*Verificaciones.*\n(.*?)(?=##|\Z)', texto, re.DOTALL | re.IGNORECASE)
    if ver_section:
        for line in ver_section.group(1).split('\n'):
            line = line.strip()
            if '✅' in line:
                verificaciones.append(VerificacionDetalle(nombre=line[:60], resultado="OK", detalle=line))
            elif '❌' in line:
                verificaciones.append(VerificacionDetalle(nombre=line[:60], resultado="FALLO", detalle=line))
            elif '⚠️' in line:
                verificaciones.append(VerificacionDetalle(nombre=line[:60], resultado="ALERTA", detalle=line))

    return BertaResponse(
        expediente_id=parte.expediente_id,
        codigo_cas_recibido=parte.codigo_cas,
        timestamp_analisis=datetime.utcnow(),
        id_analisis=id_analisis,
        decision=decision,
        codigo_cas_respuesta=codigo_respuesta,
        confianza=confianza,
        estado_cola=estado_cola,
        requiere_accion_humana=requiere_humano,
        resumen_caso=resumen,
        verificaciones=verificaciones,
        justificacion_normativa=justificacion,
        alertas=alertas,
        nota_expediente=nota,
        respuesta_completa=texto,
    )


async def _run_berta(prompt: str) -> str:
    """Ejecuta el agente Berta con el prompt dado y devuelve el texto de respuesta."""
    runner = InMemoryRunner(agent=root_agent, app_name="berta_api")
    session = await runner.session_service.create_session(
        app_name="berta_api", user_id="api_user"
    )
    content = Content(role="user", parts=[Part(text=prompt)])
    full_response = ""
    async for event in runner.run_async(
        user_id="api_user",
        session_id=session.id,
        new_message=content,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    full_response += part.text
    return full_response


# ─────────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────────

@app.get("/health", tags=["Sistema"])
async def health():
    """Health check del servidor."""
    return {"status": "ok", "agente": root_agent.name, "timestamp": datetime.utcnow().isoformat()}


@app.post("/cas/parte", response_model=BertaResponse, tags=["CAS"])
async def procesar_parte(parte: ParteInput):
    """
    **Endpoint principal de integración.**

    Recibe un parte CAS del sistema de IT, lo procesa con Berta
    y devuelve la decisión estructurada encolada para validación humana.

    - `estado_cola = PROCESADO_AUTOMATICAMENTE` → se puede ejecutar directamente
    - `estado_cola = PENDIENTE_VALIDACION` → el tramitador debe revisar antes de emitir
    - `estado_cola = REQUIERE_INTERVENCION_MANUAL` → revisión obligatoria, posible fraude
    """
    id_analisis = nueva_id()
    prompt = _build_prompt(parte)

    try:
        texto_berta = await _run_berta(prompt)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error al consultar al agente Berta: {str(e)}")

    response = _parse_berta_response(texto_berta, parte, id_analisis)
    encolar_analisis(response)
    return response


@app.get("/cas/cola", response_model=list[ItemCola], tags=["Cola de Validación"])
async def listar_cola(
    estado: Optional[str] = Query(None, description="Filtrar por estado: PENDIENTE, APROBADO, RECHAZADO, MODIFICADO"),
    limit: int = Query(50, ge=1, le=200),
):
    """Lista los análisis de Berta en la cola de validación humana."""
    return obtener_cola(estado=estado, limit=limit)


@app.get("/cas/cola/{id_analisis}", response_model=BertaResponse, tags=["Cola de Validación"])
async def detalle_analisis(id_analisis: str):
    """Devuelve el análisis completo de Berta para un caso específico."""
    analisis = obtener_analisis(id_analisis)
    if not analisis:
        raise HTTPException(status_code=404, detail=f"Análisis {id_analisis} no encontrado")
    return analisis


@app.patch("/cas/cola/{id_analisis}/validar", tags=["Cola de Validación"])
async def validar_caso(id_analisis: str, validacion: ValidacionHumana):
    """
    El tramitador humano aprueba, rechaza o modifica la propuesta de Berta.

    - `APROBADO` → se acepta la decisión de Berta tal cual
    - `RECHAZADO` → el tramitador no acepta y tomará una decisión diferente
    - `MODIFICADO` → el tramitador acepta con cambios (indicar `codigo_cas_final`)
    """
    ok = validar_analisis(id_analisis, validacion)
    if not ok:
        raise HTTPException(status_code=404, detail=f"Análisis {id_analisis} no encontrado")
    return {
        "status": "ok",
        "id_analisis": id_analisis,
        "validacion": validacion.validacion.value,
        "tramitador": validacion.tramitador_id,
        "timestamp": datetime.utcnow().isoformat(),
    }


# ─────────────────────────────────────────────
# ENDPOINTS SIAX / ServiciosGemini
# ─────────────────────────────────────────────

@app.get("/cas/siax/test", tags=["SIAX"])
async def siax_test_conexion():
    """
    Verifica la conectividad con el servicio SIAX (ServiciosGemini).
    Llama al método GetTest() que no requiere autenticación.
    """
    result = siax_client.test_conexion()
    if not result.get("ok"):
        raise HTTPException(status_code=502, detail=result.get("mensaje", "Error de conexión SIAX"))
    return result


@app.post("/cas/siax/analizar-caso", tags=["SIAX"])
async def siax_analizar_caso(request: SiaxAnalisisCasoRequest):
    """
    **Botón 1 — Analizar Caso Completo.**

    Consulta SIAX para obtener todas las secuencias y mensajes de un caso CAS,
    luego usa Berta para analizar cuáles requieren respuesta y qué acciones tomar.

    Flujo:
    1. Llama a SIAX → ObtenerCas(idCas)
    2. Enriquece cada mensaje con emisor, caducidad, códigos de respuesta válidos
    3. Pasa el contexto a Berta para análisis inteligente
    4. Devuelve los datos + el análisis de Berta
    """
    # 1. Obtener datos de SIAX
    datos_siax = siax_client.obtener_cas(request.id_cas)

    if not datos_siax.get("ok"):
        raise HTTPException(
            status_code=502,
            detail=f"Error al consultar SIAX: {datos_siax.get('error', 'Error desconocido')}"
        )

    # 2. Construir prompt para Berta con los datos de SIAX
    prompt = _build_siax_caso_prompt(datos_siax)

    # 3. Ejecutar Berta
    try:
        analisis_berta = await _run_berta(prompt)
    except Exception as e:
        analisis_berta = f"Error al consultar a Berta: {str(e)}"

    # 4. Extraer respuesta recomendada
    respuesta_recomendada = _extraer_respuesta_recomendada(analisis_berta)

    # 5. Devolver datos + análisis
    return {
        "id_cas": request.id_cas,
        "total_secuencias": datos_siax["total_secuencias"],
        "total_mensajes": datos_siax["total_mensajes"],
        "secuencias_respondibles": datos_siax["secuencias_respondibles"],
        "secuencias": datos_siax["secuencias"],
        "analisis_berta": analisis_berta,
        "respuesta_recomendada": respuesta_recomendada,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/cas/siax/analizar-mensaje", tags=["SIAX"])
async def siax_analizar_mensaje(request: SiaxAnalisisMensajeRequest):
    """
    **Botón 2 — Analizar Mensaje y Recomendar Respuesta.**

    Consulta SIAX para obtener el contexto de un mensaje específico,
    luego usa Berta para recomendar con qué código CAS responder.

    Flujo:
    1. Llama a SIAX → ObtenerCas(idCas)
    2. Localiza el mensaje por su ID dentro de las secuencias
    3. Construye el contexto (historial de la secuencia)
    4. Pasa todo a Berta para que recomiende la respuesta
    5. Devuelve los datos del mensaje + recomendación de Berta
    """
    # 1. Obtener datos de SIAX
    datos_siax = siax_client.obtener_cas(request.id_cas)

    if not datos_siax.get("ok"):
        raise HTTPException(
            status_code=502,
            detail=f"Error al consultar SIAX: {datos_siax.get('error', 'Error desconocido')}"
        )

    # 2. Buscar el mensaje específico
    mensaje_encontrado = None
    secuencia_contexto = None

    for sec in datos_siax.get("secuencias", []):
        for msg in sec.get("mensajes", []):
            if msg["id"] == request.id_mensaje:
                mensaje_encontrado = msg
                secuencia_contexto = sec
                break
        if mensaje_encontrado:
            break

    if not mensaje_encontrado:
        raise HTTPException(
            status_code=404,
            detail=f"Mensaje {request.id_mensaje} no encontrado en el caso CAS {request.id_cas}"
        )

    # 3. Construir prompt para Berta
    prompt = _build_siax_mensaje_prompt(datos_siax, mensaje_encontrado, secuencia_contexto)

    # 4. Ejecutar Berta
    try:
        analisis_berta = await _run_berta(prompt)
    except Exception as e:
        analisis_berta = f"Error al consultar a Berta: {str(e)}"

    # 5. Extraer respuesta recomendada del análisis de Berta
    respuesta_recomendada = _extraer_respuesta_recomendada(analisis_berta)

    # 6. Devolver datos del mensaje + análisis
    return {
        "id_cas": request.id_cas,
        "id_mensaje": request.id_mensaje,
        "referencia_cas": secuencia_contexto["referencia_cas"],
        "mensaje": mensaje_encontrado,
        "historial_secuencia": secuencia_contexto["mensajes"],
        "analisis_berta": analisis_berta,
        "respuesta_recomendada": respuesta_recomendada,
        "timestamp": datetime.utcnow().isoformat(),
    }


# ─────────────────────────────────────────────
# Helpers SIAX
# ─────────────────────────────────────────────

def _extraer_respuesta_recomendada(analisis_berta: str) -> dict:
    """
    Extrae la respuesta recomendada del análisis de texto de Berta.
    Busca múltiples patrones en el texto para encontrar el código que Berta recomienda.
    
    Returns:
        Dict con {codigo, nombre, justificacion, confianza}
    """
    from cas_codes import CAS_CODES
    
    if not isinstance(analisis_berta, str):
        return {
            "codigo": None,
            "nombre": None,
            "justificacion": "No se pudo analizar la respuesta de Berta.",
            "confianza": "BAJA",
        }
    
    codigo = None
    justificacion = ""
    confianza = "MEDIA"
    
    # Lista de patrones regex ordenados por prioridad (el primero que coincida gana)
    patrones = [
        # "RECOMENDACIÓN PRINCIPAL: código 271"
        r'RECOMENDACI[OÓ]N\s+PRINCIPAL[:\s]+[Cc]ó?digo\s+[\'"]?(\d+)[\'"]?',
        # "**Código CAS**: 271" o "**Código CAS**: '271'"
        r'\*\*C[oó]digo\s*CAS\*\*[:\s]+[\'"]?(\d+)[\'"]?',
        # "**Código**: 271"
        r'\*\*C[oó]digo\*\*[:\s]+[\'"]?(\d+)[\'"]?',
        # "se recomienda enviar código '368'" / "se recomienda enviar código 368"
        r'[Ss]e\s+recomienda\s+(?:enviar|responder\s+con|usar)\s+(?:el\s+)?c[oó]digo\s+[\'"]?(\d+)[\'"]?',
        # "se debe proceder con el envío del código '368'"
        r'[Ss]e\s+debe\s+proceder\s+con\s+(?:el\s+)?(?:envío\s+del\s+)?c[oó]digo\s+[\'"]?(\d+)[\'"]?',
        # "recomendar/enviar/responder/usar código '368'" / "código 368"
        r'(?:responder|recomendar|enviar|usar)\s+(?:con\s+)?(?:el\s+)?c[oó]digo\s+[\'"]?(\d+)[\'"]?',
        # "código de respuesta: 271" / "código respuesta '271'"
        r'c[oó]digo\s+(?:de\s+)?respuesta[:\s]+[\'"]?(\d+)[\'"]?',
        # "enviar un '281'" o "enviar un 281"
        r'enviar\s+un\s+[\'"]?(\d{3})[\'"]?',
        # "con código '368'" (genérico)
        r'con\s+(?:el\s+)?c[oó]digo\s+[\'"]?(\d+)[\'"]?',
        # "código '368' (Solicita..." — código entre comillas seguido de paréntesis
        r'c[oó]digo\s+[\'"](\d+)[\'"](?:\s*\()',
    ]
    
    for patron in patrones:
        m = re.search(patron, analisis_berta, re.IGNORECASE)
        if m:
            candidato = m.group(1)
            # Verificar que sea un código CAS válido
            if candidato in CAS_CODES:
                codigo = candidato
                # Extraer contexto como justificación
                start = max(0, m.start() - 50)
                end = min(len(analisis_berta), m.end() + 300)
                justificacion = analisis_berta[start:end].strip()
                break
            elif not codigo:
                # Guardar como candidato aunque no esté en CAS_CODES
                codigo = candidato
                start = max(0, m.start() - 50)
                end = min(len(analisis_berta), m.end() + 300)
                justificacion = analisis_berta[start:end].strip()
    
    # Fallback: buscar cualquier número de 3 dígitos que sea un código CAS válido
    # mencionado después de palabras clave de recomendación
    if not codigo:
        m = re.search(r'(?:recomiend|suger|propon)\w*[^.]{0,30}?[\'"]?(\d{3})[\'"]?', analisis_berta, re.IGNORECASE)
        if m and m.group(1) in CAS_CODES:
            codigo = m.group(1)
            start = max(0, m.start() - 20)
            end = min(len(analisis_berta), m.end() + 200)
            justificacion = analisis_berta[start:end].strip()
    
    # Buscar confianza
    texto_upper = analisis_berta.upper()
    if "CONFIANZA: ALTA" in texto_upper or "ALTA (>" in texto_upper:
        confianza = "ALTA"
    elif "CONFIANZA: BAJA" in texto_upper or "BAJA (<" in texto_upper:
        confianza = "BAJA"
    
    # Extraer justificación de la sección de decisión si no se encontró arriba
    if not justificacion:
        just_section = re.search(r'(?:Decisi[oó]n|Justificaci[oó]n|Motivo)[:\s]+(.{20,500})', analisis_berta, re.IGNORECASE)
        if just_section:
            justificacion = just_section.group(1).strip()
    
    # Obtener nombre del código
    nombre = None
    if codigo and codigo in CAS_CODES:
        nombre = CAS_CODES[codigo].get("nombre", "Desconocido")
    elif codigo:
        nombre = f"Código {codigo} (no encontrado en catálogo)"
    
    return {
        "codigo": codigo,
        "nombre": nombre,
        "justificacion": justificacion or "Sin justificación extraída del análisis.",
        "confianza": confianza,
    }

def _build_siax_caso_prompt(datos_siax: dict) -> str:
    """Construye el prompt para que Berta analice un caso completo de SIAX."""
    id_cas = datos_siax["id_cas"]
    total_sec = datos_siax["total_secuencias"]
    total_msg = datos_siax["total_mensajes"]
    respondibles = datos_siax["secuencias_respondibles"]

    prompt = f"""ANÁLISIS DE CASO SIAX — ID CAS: {id_cas}

📡 Datos obtenidos en tiempo real desde SIAX (ServiciosGemini).
Estos datos son REALES, no simulados.

Resumen:
- Total de secuencias: {total_sec}
- Total de mensajes: {total_msg}
- Secuencias que requieren acción: {respondibles}

"""

    for i, sec in enumerate(datos_siax.get("secuencias", []), 1):
        prompt += f"\n{'='*60}\n"
        prompt += f"📋 SECUENCIA {i}: Referencia CAS {sec['referencia_cas']}\n"
        prompt += f"   Último código: {sec['ultimo_codigo']} | Necesita acción: {'SÍ ⚠️' if sec['necesita_accion'] else 'NO'}\n"
        prompt += f"   Mensajes ({sec['total_mensajes']}):\n"

        for msg in sec.get("mensajes", []):
            estado_icon = "📥" if msg["emisor"] == "HOSPITAL" else "📤"
            caduc_icon = "⏰ CADUCADO" if msg["caducado"] else ""
            ref = f" → ref:{msg['mensaje_referido']}" if msg.get("mensaje_referido") else ""
            prompt += f"     {estado_icon} [{msg['id']}] Código {msg['codigo']} ({msg['emisor']}) "
            prompt += f"| Estado: {msg['estado']} | Conv: {msg['convenio_normas']} "
            prompt += f"| Caduca: {msg['fecha_caducidad']} {caduc_icon}{ref}\n"

            if msg.get("puede_responder"):
                prompt += f"        ✅ PUEDE RESPONDER con: {msg['codigos_respuesta_validos']}\n"

        if sec.get("necesita_accion"):
            prompt += f"\n   ⚠️ ACCIÓN REQUERIDA: Responder al último mensaje (código {sec['ultimo_codigo']})\n"
            prompt += f"   Opciones de respuesta: {sec.get('codigos_respuesta_disponibles', [])}\n"

    prompt += f"""\n{'='*60}

ANALIZA TODAS las secuencias de este caso CAS.
Para cada secuencia que requiera acción:
1. Indica cuál es el mensaje pendiente de respuesta
2. Lista las opciones de código de respuesta con su significado
3. Verifica las fechas de caducidad
4. Recomienda la acción más apropiada
5. Destaca cualquier urgencia o anomalía

🚨 REGLAS CRÍTICAS ANTI-ALUCINACIONES:
- PROHIBIDO INVENTAR MENSAJES: Analiza ÚNICAMENTE los mensajes listados arriba.
- PROHIBIDO INVENTAR CÓDIGOS: Utiliza ÚNICAMENTE los 115 códigos CAS oficiales y las opciones válidas proporcionadas en el listado para cada mensaje. NUNCA sugieras códigos inventados como 99, 100, 200, 300, 900, 999, etc. NUNCA SUGIERAS UN CÓDIGO SI ESTÁ FUERA DE LAS OPCIONES DE RESPUESTA PERMITIDAS.
- Para cada secuencia con acción pendiente, indica EXPLÍCITAMENTE tu **RESPUESTA RECOMENDADA**: el código exacto que recomiendas usar y por qué.

Sigue el formato de respuesta estructurado de Berta.
"""
    return prompt


def _build_siax_mensaje_prompt(datos_siax: dict, mensaje: dict, secuencia: dict) -> str:
    """Construye el prompt para que Berta analice un mensaje específico."""
    id_cas = datos_siax["id_cas"]

    prompt = f"""ANÁLISIS DE MENSAJE SIAX — ID CAS: {id_cas} | Mensaje ID: {mensaje['id']}

📡 Datos obtenidos en tiempo real desde SIAX (ServiciosGemini).
Estos datos son REALES, no simulados.

📋 Secuencia: {secuencia['referencia_cas']}
📩 Mensaje a analizar:
- ID: {mensaje['id']}
- Código: {mensaje['codigo']}
- Emisor: {mensaje['emisor']}
- Estado: {mensaje['estado']}
- Convenio/Normas: {mensaje['convenio_normas']}
- Fecha de caducidad: {mensaje['fecha_caducidad']}
- Caducado: {'SÍ ⚠️' if mensaje['caducado'] else 'NO'}
- Mensaje referido: {mensaje.get('mensaje_referido', 'Ninguno')}
- Puede responder: {'SÍ' if mensaje.get('puede_responder') else 'NO'}
"""

    if mensaje.get("codigos_respuesta_validos"):
        prompt += f"- Códigos de respuesta válidos: {mensaje['codigos_respuesta_validos']}\n"

    prompt += f"\nHistorial completo de la secuencia ({secuencia['total_mensajes']} mensajes):\n"
    for msg in secuencia.get("mensajes", []):
        estado_icon = "📥" if msg["emisor"] == "HOSPITAL" else "📤"
        marker = " 👈 ESTE MENSAJE" if msg["id"] == mensaje["id"] else ""
        ref = f" → ref:{msg['mensaje_referido']}" if msg.get("mensaje_referido") else ""
        prompt += f"  {estado_icon} [{msg['id']}] Código {msg['codigo']} ({msg['emisor']}) "
        prompt += f"| {msg['estado']} | Conv: {msg['convenio_normas']} "
        prompt += f"| Caduca: {msg['fecha_caducidad']}{ref}{marker}\n"

    prompt += f"""\nANALIZA este mensaje específico y RECOMIENDA con qué código responder.

Debe incluir:
1. Contexto del mensaje dentro de la secuencia
2. **RECOMENDACIÓN PRINCIPAL**: Qué código de respuesta usar y POR QUÉ
3. Alternativas posibles con sus pros y contras
4. Referencia a la normativa CAS aplicable (convenio {mensaje['convenio_normas']})
5. Advertencias sobre plazos o situaciones especiales
6. Justificación normativa detallada

🚨 REGLAS CRÍTICAS ANTI-ALUCINACIONES:
- PROHIBIDO INVENTAR MENSAJES: Analiza ÚNICAMENTE los mensajes listados arriba en el 'Historial completo de la secuencia'.
- PROHIBIDO INVENTAR CÓDIGOS CAS: Utiliza ÚNICAMENTE los 115 códigos CAS oficiales. NUNCA utilices ni recomiendes códigos inventados que no existan en la norma CAS. NUNCA SUGIERAS UN CÓDIGO SI ESTÁ FUERA DE LAS OPCIONES DE RESPUESTA PERMITIDAS.
- DEBES indicar EXPLÍCITAMENTE tu **RESPUESTA RECOMENDADA**: el código exacto que recomiendas y la justificación normativa.

Sigue el formato de respuesta estructurado de Berta.
"""
    return prompt
