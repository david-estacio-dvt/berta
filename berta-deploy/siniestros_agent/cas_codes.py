"""
cas_codes.py - Máquina de estados y definiciones de códigos CAS.

Contiene toda la lógica de secuencia de códigos del Convenio de Asistencia
Sanitaria (CAS) para convenios de Sanidad Pública, Privada y Emergencias.
"""

# ============================================================
# CÓDIGOS CAS - CONVENIO SANITARIO PÚBLICO
# ============================================================
# Basado en: 212_CAS_ESP_DOC_NORMAS_PROCEDIMIENTO_GENERAL
# y documentación de Documentos Estándar CS/EA

CAS_CODES = {
    # --- PARTE INICIAL (Hospital → Aseguradora) ---
    "100": {
        "nombre": "Parte de Asistencia Inicial",
        "descripcion": "El centro hospitalario comunica la asistencia inicial al lesionado.",
        "emisor": "HOSPITAL",
        "tipo": "INICIO",
        "datos_obligatorios": [
            "fecha_ocurrencia", "matricula_vehiculo", "datos_lesionado",
            "tipo_lesion", "posicion_vehiculo", "datos_hospital"
        ],
        "plazo_respuesta_dias": 5,
    },
    "171": {
        "nombre": "Parte de Asistencia Inicial (alternativo)",
        "descripcion": "Código alternativo de parte inicial. Código inicial 171 ó 101. Matrícula FIV. Datos del lesionado.",
        "emisor": "HOSPITAL",
        "tipo": "INICIO",
        "datos_obligatorios": [
            "fecha_ocurrencia", "matricula_fiv", "datos_lesionado",
            "tipo_lesion", "datos_hospital"
        ],
        "plazo_respuesta_dias": 5,
    },
    "101": {
        "nombre": "Parte de Asistencia Inicial (variante)",
        "descripcion": "Código variante de parte inicial.",
        "emisor": "HOSPITAL",
        "tipo": "INICIO",
        "datos_obligatorios": [
            "fecha_ocurrencia", "matricula_vehiculo", "datos_lesionado",
            "tipo_lesion", "datos_hospital"
        ],
        "plazo_respuesta_dias": 5,
    },

    # --- RESPUESTAS ASEGURADORA ---
    "200": {
        "nombre": "Aceptación del Parte",
        "descripcion": "La aseguradora acepta el parte de asistencia.",
        "emisor": "ASEGURADORA",
        "tipo": "RESPUESTA",
        "datos_obligatorios": ["numero_expediente"],
        "plazo_respuesta_dias": None,
    },
    "300": {
        "nombre": "Aceptación con Reservas",
        "descripcion": "La aseguradora acepta con ciertas condiciones o reservas.",
        "emisor": "ASEGURADORA",
        "tipo": "RESPUESTA",
        "datos_obligatorios": ["numero_expediente", "motivo_reserva"],
        "plazo_respuesta_dias": None,
    },
    "301": {
        "nombre": "Solicitud de Documentación Adicional",
        "descripcion": "La aseguradora solicita más documentación al hospital.",
        "emisor": "ASEGURADORA",
        "tipo": "SOLICITUD_DOC",
        "datos_obligatorios": ["documentos_requeridos"],
        "plazo_respuesta_dias": 15,
    },

    # --- INTERCAMBIO DE DOCUMENTACIÓN ---
    "328": {
        "nombre": "Envío de Documentación Clínica (Hospital)",
        "descripcion": "El hospital envía documentación médica/clínica. Formato XML/TXT con datos diagnósticos y de continuidad.",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
        "datos_obligatorios": ["documentos_adjuntos"],
        "plazo_respuesta_dias": None,
    },
    "329": {
        "nombre": "Envío de Documentación Clínica (Hospital - variante)",
        "descripcion": "Variante de envío de documentación clínica. Similar al 328 con datos adicionales.",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
        "datos_obligatorios": ["documentos_adjuntos"],
        "plazo_respuesta_dias": None,
    },
    "400": {
        "nombre": "Recepción de Documentación",
        "descripcion": "Confirmación de recepción de la documentación enviada.",
        "emisor": "ASEGURADORA",
        "tipo": "CONFIRMACION",
        "datos_obligatorios": [],
        "plazo_respuesta_dias": None,
    },

    # --- FACTURACIÓN ---
    "500": {
        "nombre": "Factura / Cierre de Asistencia",
        "descripcion": "El hospital envía factura o cierre de la asistencia. Código 500 indica fin del proceso.",
        "emisor": "HOSPITAL",
        "tipo": "FACTURACION",
        "datos_obligatorios": ["importe_total", "desglose_servicios"],
        "plazo_respuesta_dias": 30,
    },
    "501": {
        "nombre": "Factura Parcial",
        "descripcion": "El hospital envía factura parcial de servicios prestados.",
        "emisor": "HOSPITAL",
        "tipo": "FACTURACION",
        "datos_obligatorios": ["importe_parcial", "servicios"],
        "plazo_respuesta_dias": 30,
    },

    # --- RESOLUCIÓN ---
    "600": {
        "nombre": "Aceptación de Factura",
        "descripcion": "La aseguradora acepta la factura presentada.",
        "emisor": "ASEGURADORA",
        "tipo": "PAGO",
        "datos_obligatorios": ["importe_aceptado"],
        "plazo_respuesta_dias": None,
    },
    "700": {
        "nombre": "Pago Realizado",
        "descripcion": "Confirmación de que el pago ha sido realizado.",
        "emisor": "ASEGURADORA",
        "tipo": "PAGO",
        "datos_obligatorios": ["importe_pagado", "fecha_pago"],
        "plazo_respuesta_dias": None,
    },

    # --- REHÚSE / RECHAZO ---
    "828": {
        "nombre": "Envío Documentación para Rehúse",
        "descripcion": "Documentación asociada a un rehúse. Formato XML/TXT.",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
        "datos_obligatorios": ["motivo_rehuse"],
        "plazo_respuesta_dias": None,
    },
    "900": {
        "nombre": "Rehúse / Rechazo",
        "descripcion": "La aseguradora rechaza el parte o la factura.",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
        "datos_obligatorios": ["motivo_rechazo"],
        "plazo_respuesta_dias": None,
    },
    "901": {
        "nombre": "Rehúse Parcial",
        "descripcion": "La aseguradora rechaza parcialmente (acepta parte, rechaza otra).",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
        "datos_obligatorios": ["motivo_rechazo_parcial", "importe_aceptado"],
        "plazo_respuesta_dias": None,
    },

    # --- BAJA ---
    "999": {
        "nombre": "Baja del Expediente",
        "descripcion": "Cierre definitivo del expediente CAS.",
        "emisor": "AMBOS",
        "tipo": "CIERRE",
        "datos_obligatorios": ["motivo_baja"],
        "plazo_respuesta_dias": None,
    },
}

# ============================================================
# MÁQUINA DE ESTADOS - TRANSICIONES VÁLIDAS
# ============================================================
# Clave: código actual → Lista de códigos siguientes válidos

CAS_TRANSITIONS = {
    "INICIO": ["100", "101", "171"],  # Códigos que pueden iniciar un diálogo
    
    # Desde partes iniciales
    "100": ["200", "300", "301", "900", "999"],
    "101": ["200", "300", "301", "900", "999"],
    "171": ["200", "300", "301", "900", "999"],
    
    # Desde aceptación
    "200": ["328", "329", "500", "501", "999"],
    "300": ["328", "329", "500", "501", "301", "999"],
    
    # Desde solicitud de documentación
    "301": ["328", "329", "400", "900", "999"],
    
    # Desde envío de documentación
    "328": ["400", "301", "600", "900", "901", "999"],
    "329": ["400", "301", "600", "900", "901", "999"],
    
    # Desde confirmación de recepción
    "400": ["328", "329", "500", "501", "600", "900", "901", "999"],
    
    # Desde facturación
    "500": ["600", "700", "900", "901", "828", "999"],
    "501": ["600", "700", "900", "901", "501", "500", "999"],
    
    # Desde aceptación de factura
    "600": ["700", "999"],
    
    # Desde pago
    "700": ["999"],
    
    # Desde rehúse
    "828": ["900", "999"],
    "900": ["999"],
    "901": ["500", "501", "999"],
    
    # Cierre - no hay transición posible
    "999": [],
}

# ============================================================
# TIPOS DE CONVENIO
# ============================================================

CONVENIO_TIPOS = {
    "PUBLICO": {
        "nombre": "Convenio Sanitario Público",
        "codigo_inicio": ["100", "101", "171"],
        "descripcion": "Convenio entre entidades aseguradoras y servicios de salud públicos.",
    },
    "PRIVADO": {
        "nombre": "Convenio Clínicas Privadas",
        "codigo_inicio": ["100", "101"],
        "descripcion": "Convenio entre entidades aseguradoras y clínicas privadas.",
    },
    "EMERGENCIAS": {
        "nombre": "Convenio de Emergencias",
        "codigo_inicio": ["100"],
        "descripcion": "Convenio para servicios de emergencia y ambulancia.",
    },
}

# ============================================================
# MOTIVOS DE REHÚSE ESTÁNDAR
# ============================================================

MOTIVOS_REHUSE = {
    "R01": "Póliza no vigente en fecha de ocurrencia",
    "R02": "Vehículo no asegurado",
    "R03": "Lesionado no identificado como ocupante",
    "R04": "Fecha de ocurrencia fuera de periodo convenio",
    "R05": "Hospital no adherido al convenio",
    "R06": "Lesión no coherente con dinámica del accidente",
    "R07": "Documentación insuficiente o ilegible",
    "R08": "Factura excede baremos del convenio",
    "R09": "Duplicidad de parte (ya existe expediente para este lesionado/siniestro)",
    "R10": "Siniestro no reconocido / sin parte de accidente",
    "R11": "Tratamiento no justificado por la lesión declarada",
    "R12": "Plazo de presentación superado",
}

# ============================================================
# FUNCIONES DE VALIDACIÓN
# ============================================================

def validate_transition(current_code: str, next_code: str) -> dict:
    """
    Valida si la transición entre dos códigos CAS es válida.
    
    Returns:
        Dict con {valid: bool, message: str, allowed_codes: list}
    """
    if current_code not in CAS_TRANSITIONS:
        return {
            "valid": False,
            "message": f"Código actual '{current_code}' no reconocido en la máquina de estados.",
            "allowed_codes": []
        }
    
    allowed = CAS_TRANSITIONS[current_code]
    
    if next_code in allowed:
        next_info = CAS_CODES.get(next_code, {})
        return {
            "valid": True,
            "message": f"Transición {current_code} → {next_code} ({next_info.get('nombre', 'Desconocido')}) es VÁLIDA.",
            "allowed_codes": allowed
        }
    else:
        return {
            "valid": False,
            "message": f"Transición {current_code} → {next_code} NO es válida. Códigos permitidos desde {current_code}: {allowed}",
            "allowed_codes": allowed
        }


def get_code_info(code: str) -> dict:
    """Devuelve información completa sobre un código CAS."""
    if code in CAS_CODES:
        info = CAS_CODES[code].copy()
        info["codigo"] = code
        info["transiciones_validas"] = CAS_TRANSITIONS.get(code, [])
        return info
    return {"error": f"Código '{code}' no encontrado en el catálogo CAS."}


def get_required_action(code: str) -> str:
    """Devuelve la acción requerida por la aseguradora para un código recibido."""
    info = CAS_CODES.get(code, {})
    tipo = info.get("tipo", "")
    plazo = info.get("plazo_respuesta_dias")
    
    actions = {
        "INICIO": f"Recibido parte inicial. Verificar datos y responder en {plazo} días con código 200 (aceptar), 300 (aceptar con reservas), 301 (solicitar documentación) o 900 (rehusar).",
        "DOCUMENTACION": "Documentación recibida. Revisar contenido y responder con 400 (confirmar recepción), solicitar más con 301, o proceder a facturación.",
        "FACTURACION": f"Factura recibida. Revisar importes contra baremos y responder en {plazo} días con 600 (aceptar), 900 (rehusar) o 901 (rehúse parcial).",
        "REHUSE": "Rehúse recibido. Registrar motivo y cerrar expediente si procede.",
        "CIERRE": "Expediente cerrado. No requiere acción adicional.",
    }
    
    return actions.get(tipo, f"Código {code} recibido. Consultar normativa para determinar acción.")
