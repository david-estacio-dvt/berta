"""
cas_codes.py - Máquina de estados y definiciones de códigos CAS.

Contiene toda la lógica de secuencia de códigos del Convenio de Asistencia
Sanitaria (CAS) para convenios de Sanidad Pública, Privada y Emergencias.

IMPORTANTE: Los códigos aquí definidos son los ÚNICOS códigos oficiales
válidos según la normativa 212_CAS_ESP_DOC V42 (06/06/2024).
NO SE PUEDE USAR NINGÚN CÓDIGO QUE NO ESTÉ EN ESTA LISTA.
"""

# ============================================================
# CÓDIGOS CAS OFICIALES - Normativa V42 (06/06/2024)
# ============================================================
# Fuente: 212_CAS_ESP_DOC_NORMAS_PROCEDIMIENTO_GENERAL_V42
# Total: 115 códigos únicos oficiales
# Emisores: CH=Centro Hospitalario, EA=Entidad Aseguradora,
#           CS=Comisión/Subcomisión, CCS=Centro Concertado Sanitario

CAS_CODES = {
    # --- Códigos 0xx: Datos y liquidación ---
    "47": {
        "nombre": "Envío datos liquidación",
        "descripcion": "Envío datos liquidación",
        "emisor": "HOSPITAL",
        "tipo": "INICIO",
    },
    # --- Códigos 1xx: Partes iniciales e informativos ---
    "101": {
        "nombre": "PA Urgencias",
        "descripcion": "PA Urgencias",
        "emisor": "HOSPITAL",
        "tipo": "INICIO",
    },
    "102": {
        "nombre": "PA urgencias modificado",
        "descripcion": "PA urgencias modificado",
        "emisor": "HOSPITAL",
        "tipo": "INICIO",
    },
    "170": {
        "nombre": "Parte de comunicación de lesiones",
        "descripcion": "Parte de comunicación de lesiones",
        "emisor": "SISTEMA",
        "tipo": "INICIO",
    },
    "171": {
        "nombre": "Envío parte de asistencia",
        "descripcion": "Envío parte de asistencia / Parte de primera Asistencia ambulatoria u hospitalaria",
        "emisor": "HOSPITAL",
        "tipo": "INICIO",
    },
    "172": {
        "nombre": "Envío nuevo parte de asistencia modificado",
        "descripcion": "Envío nuevo parte de asistencia modificado / PA ambulatorio modificado",
        "emisor": "HOSPITAL",
        "tipo": "INICIO",
    },
    "173": {
        "nombre": "Envía parte de asistencia de reingreso",
        "descripcion": "Envía parte de asistencia de reingreso / PA reingreso/PA continuación gestión lesionado",
        "emisor": "HOSPITAL",
        "tipo": "INICIO",
    },
    "174": {
        "nombre": "Envía parte de asistencia de reingreso modificado",
        "descripcion": "Envía parte de asistencia de reingreso modificado",
        "emisor": "HOSPITAL",
        "tipo": "INICIO",
    },
    "175": {
        "nombre": "Envío parte de asistencia informativo",
        "descripcion": "Envío parte de asistencia informativo",
        "emisor": "HOSPITAL",
        "tipo": "INICIO",
    },
    "176": {
        "nombre": "Envío parte de asistencia de entidad no adherida a convenio",
        "descripcion": "Envío parte de asistencia de entidad no adherida a convenio",
        "emisor": "HOSPITAL",
        "tipo": "INICIO",
    },
    "181": {
        "nombre": "Envío factura",
        "descripcion": "Envío factura",
        "emisor": "HOSPITAL",
        "tipo": "INICIO",
    },
    "191": {
        "nombre": "Envío parte de traslado interhospitalario",
        "descripcion": "Envío parte de traslado interhospitalario",
        "emisor": "HOSPITAL",
        "tipo": "INICIO",
    },
    "192": {
        "nombre": "Envío nuevo parte de traslado interhospitalario modificado",
        "descripcion": "Envío nuevo parte de traslado interhospitalario modificado",
        "emisor": "HOSPITAL",
        "tipo": "INICIO",
    },
    # --- Códigos 2xx: Aceptaciones y conformidades ---
    "201": {
        "nombre": "Acepta parte de urgencias",
        "descripcion": "Acepta parte de urgencias",
        "emisor": "ASEGURADORA",
        "tipo": "RESPUESTA",
    },
    "202": {
        "nombre": "Acepta continuación tratamiento",
        "descripcion": "Acepta continuación tratamiento",
        "emisor": "ASEGURADORA",
        "tipo": "RESPUESTA",
    },
    "203": {
        "nombre": "Acepta lesionado alta especialización",
        "descripcion": "Acepta lesionado alta especialización",
        "emisor": "ASEGURADORA",
        "tipo": "RESPUESTA",
    },
    "270": {
        "nombre": "Subcomisión acepta parte",
        "descripcion": "Subcomisión acepta parte",
        "emisor": "SISTEMA",
        "tipo": "RESPUESTA",
    },
    "271": {
        "nombre": "Acepta el parte de asistencia",
        "descripcion": "Acepta el parte de asistencia",
        "emisor": "ASEGURADORA",
        "tipo": "RESPUESTA",
    },
    "272": {
        "nombre": "Comisión acepta parte",
        "descripcion": "Comisión acepta parte",
        "emisor": "SISTEMA",
        "tipo": "RESPUESTA",
    },
    "275": {
        "nombre": "Subcomisión acepta parte tras recurso",
        "descripcion": "Subcomisión acepta parte tras recurso",
        "emisor": "SISTEMA",
        "tipo": "RESPUESTA",
    },
    "280": {
        "nombre": "Subcomisión acepta factura",
        "descripcion": "Subcomisión acepta factura",
        "emisor": "SISTEMA",
        "tipo": "RESPUESTA",
    },
    "281": {
        "nombre": "Acepta la factura",
        "descripcion": "Acepta la factura",
        "emisor": "ASEGURADORA",
        "tipo": "RESPUESTA",
    },
    "284": {
        "nombre": "Comisión acepta factura",
        "descripcion": "Comisión acepta factura",
        "emisor": "SISTEMA",
        "tipo": "RESPUESTA",
    },
    "285": {
        "nombre": "Comisión acepta pago",
        "descripcion": "Comisión acepta pago",
        "emisor": "SISTEMA",
        "tipo": "RESPUESTA",
    },
    "287": {
        "nombre": "Subcomisión acepta pago total",
        "descripcion": "Subcomisión acepta pago total",
        "emisor": "SISTEMA",
        "tipo": "RESPUESTA",
    },
    "288": {
        "nombre": "Subcomisión acepta factura tras recurso",
        "descripcion": "Subcomisión acepta factura tras recurso",
        "emisor": "SISTEMA",
        "tipo": "RESPUESTA",
    },
    # --- Códigos 3xx: Documentación y comunicaciones ---
    "301": {
        "nombre": "Comunica Continuación tratamiento",
        "descripcion": "Comunica Continuación tratamiento",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "302": {
        "nombre": "Comunica cambio de diagnóstico",
        "descripcion": "Comunica cambio de diagnóstico",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "303": {
        "nombre": "Acepta cambio de diagnóstico",
        "descripcion": "Acepta cambio de diagnóstico",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "304": {
        "nombre": "Rechaza cambio de diagnóstico",
        "descripcion": "Rechaza cambio de diagnóstico",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "305": {
        "nombre": "Solicita aclaraciones cambio de diagnóstico",
        "descripcion": "Solicita aclaraciones cambio de diagnóstico",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "306": {
        "nombre": "Envía aclaraciones cambio diagnóstico",
        "descripcion": "Envía aclaraciones cambio diagnóstico",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "308": {
        "nombre": "Acepta rechazo de factura",
        "descripcion": "Acepta rechazo de factura",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "309": {
        "nombre": "No acepta rechazo de factura",
        "descripcion": "No acepta rechazo de factura",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "310": {
        "nombre": "Vencido plazo subcomisión",
        "descripcion": "Vencido plazo subcomisión",
        "emisor": "SISTEMA",
        "tipo": "DOCUMENTACION",
    },
    "311": {
        "nombre": "Solicita informe médico de evolución",
        "descripcion": "Solicita informe médico de evolución",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "312": {
        "nombre": "Pendiente Informe de alta de urgencias",
        "descripcion": "Pendiente Informe de alta de urgencias",
        "emisor": "SISTEMA",
        "tipo": "DOCUMENTACION",
    },
    "313": {
        "nombre": "Vencido plazo subcomisión factura",
        "descripcion": "Vencido plazo subcomisión factura",
        "emisor": "SISTEMA",
        "tipo": "DOCUMENTACION",
    },
    "314": {
        "nombre": "Solicita envío hoja de firmas",
        "descripcion": "Solicita envío hoja de firmas",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "315": {
        "nombre": "Solicito autorización pruebas diagnósticas",
        "descripcion": "Solicito autorización pruebas diagnósticas",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "316": {
        "nombre": "Autorizo pruebas diagnósticas",
        "descripcion": "Autorizo pruebas diagnósticas",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "317": {
        "nombre": "No autorizo pruebas diagnósticas",
        "descripcion": "No autorizo pruebas diagnósticas",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "318": {
        "nombre": "Ampliación plazo",
        "descripcion": "Ampliación plazo",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "319": {
        "nombre": "Acepto Infiltraciones-bloqueos facetarios, nerviosos",
        "descripcion": "Acepto Infiltraciones-bloqueos facetarios, nerviosos",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "320": {
        "nombre": "Rechazo Infiltraciones-bloqueos facetarios, nerviosos",
        "descripcion": "Rechazo Infiltraciones-bloqueos facetarios, nerviosos",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "321": {
        "nombre": "Acepto ondas de choque radiales",
        "descripcion": "Acepto ondas de choque radiales",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "322": {
        "nombre": "Rechazo ondas de choque radiales",
        "descripcion": "Rechazo ondas de choque radiales",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "323": {
        "nombre": "Acepto ondas de choque focales",
        "descripcion": "Acepto ondas de choque focales",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "324": {
        "nombre": "Rechazo ondas de choque focales",
        "descripcion": "Rechazo ondas de choque focales",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "325": {
        "nombre": "Procede reducción de tarifas",
        "descripcion": "Procede reducción de tarifas",
        "emisor": "SISTEMA",
        "tipo": "DOCUMENTACION",
    },
    "326": {
        "nombre": "Subcomisión resuelve que procede el cambio de diagnóstico",
        "descripcion": "Subcomisión resuelve que procede el cambio de diagnóstico",
        "emisor": "SISTEMA",
        "tipo": "DOCUMENTACION",
    },
    "327": {
        "nombre": "Subcomisión resuelve que no procede el cambio de diagnóstico",
        "descripcion": "Subcomisión resuelve que no procede el cambio de diagnóstico",
        "emisor": "SISTEMA",
        "tipo": "DOCUMENTACION",
    },
    "360": {
        "nombre": "Cambio de referencia del expediente",
        "descripcion": "Cambio de referencia del expediente",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "361": {
        "nombre": "EA solicita módulo reducido",
        "descripcion": "EA solicita módulo reducido",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "362": {
        "nombre": "Solicita información aclaratoria",
        "descripcion": "Solicita información aclaratoria",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "363": {
        "nombre": "Envía información aclaratoria",
        "descripcion": "Envía información aclaratoria",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "364": {
        "nombre": "CS confirma aplica módulo reducido",
        "descripcion": "CS confirma aplica módulo reducido",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "365": {
        "nombre": "Justificación de envío fuera de plazo",
        "descripcion": "Justificación de envío fuera de plazo",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "366": {
        "nombre": "Documentación sin catalogar (CH)",
        "descripcion": "Documentación sin catalogar",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "367": {
        "nombre": "Documentación sin catalogar (EA)",
        "descripcion": "Documentación sin catalogar",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "368": {
        "nombre": "Solicita aclaración factura",
        "descripcion": "Solicita aclaración factura",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "369": {
        "nombre": "Envía aclaración factura",
        "descripcion": "Envía aclaración factura",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "370": {
        "nombre": "Solicita autorización inicio tratamiento rehabilitador fuera termino municipal",
        "descripcion": "Solicita autorización inicio tratamiento rehabilitador fuera termino municipal",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "371": {
        "nombre": "Autoriza tratamiento rehabilitador fuera del término municipal",
        "descripcion": "Autoriza tratamiento rehabilitador fuera del término municipal",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "372": {
        "nombre": "No autoriza tratamiento rehabilitador fuera del término municipal",
        "descripcion": "No autoriza tratamiento rehabilitador fuera del término municipal",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "373": {
        "nombre": "CS rechaza aplicar módulo reducido",
        "descripcion": "CS rechaza aplicar módulo reducido",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "374": {
        "nombre": "Justificante de no aseguramiento",
        "descripcion": "Justificante de no aseguramiento",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "375": {
        "nombre": "Solicita aclaración declaración responsable",
        "descripcion": "Solicita aclaración declaración responsable",
        "emisor": "SISTEMA",
        "tipo": "DOCUMENTACION",
    },
    "376": {
        "nombre": "Envía aclaración declaración responsable",
        "descripcion": "Envía aclaración declaración responsable",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "377": {
        "nombre": "Envía información alegaciones parte (CH)",
        "descripcion": "Envía información alegaciones parte",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "378": {
        "nombre": "Envía información alegaciones parte (EA)",
        "descripcion": "Envía información alegaciones parte",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "379": {
        "nombre": "Envía información alegaciones factura (CH)",
        "descripcion": "Envía información alegaciones factura",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "380": {
        "nombre": "Envía información alegaciones factura (EA)",
        "descripcion": "Envía información alegaciones factura",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "381": {
        "nombre": "Entidad notifica pago de la factura",
        "descripcion": "Entidad notifica pago de la factura",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "383": {
        "nombre": "EA diálogo adicional aplicación módulo",
        "descripcion": "EA diálogo adicional aplicación módulo",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "384": {
        "nombre": "CS diálogo adicional aplicación módulo",
        "descripcion": "CS diálogo adicional aplicación módulo",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "387": {
        "nombre": "EA comunica límite del conductor",
        "descripcion": "EA comunica límite del conductor",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "390": {
        "nombre": "EA envía aclaraciones PA, solicitud subcomisión",
        "descripcion": "EA envía aclaraciones Parte Asistencia, solicitud subcomisión",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "391": {
        "nombre": "CH envía aclaraciones PA, solicitud subcomisión",
        "descripcion": "CH envía aclaraciones Parte Asistencia, solicitud subcomisión",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "392": {
        "nombre": "CH envía aclaraciones PA, solicitud Comisión",
        "descripcion": "CH envía aclaraciones Parte Asistencia, solicitud Comisión",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "393": {
        "nombre": "CH envía aclaraciones Factura, solicitud Comisión",
        "descripcion": "CH envía aclaraciones Factura, solicitud Comisión",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "394": {
        "nombre": "EA envía aclaraciones Factura, solicitud Comisión",
        "descripcion": "EA envía aclaraciones Factura, solicitud Comisión",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "395": {
        "nombre": "CH envía aclaraciones Factura, solicitud Comisión",
        "descripcion": "CH envía aclaraciones Factura, solicitud Comisión",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "398": {
        "nombre": "EA envía aclaraciones PA, solicitud Comisión",
        "descripcion": "EA envía aclaraciones Parte Asistencia, solicitud Comisión",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "399": {
        "nombre": "EA envía aclaraciones Factura, solicitud Subcomisión",
        "descripcion": "EA envía aclaraciones Factura, solicitud Subcomisión",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    # --- Códigos 4xx: Rechazos de partes y facturas ---
    "401": {
        "nombre": "Parte de urgencias no cumplimentado correctamente",
        "descripcion": "Parte de urgencias no cumplimentado correctamente",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "403": {
        "nombre": "Rechaza lesionado alta especialización",
        "descripcion": "Rechaza lesionado alta especialización",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "421": {
        "nombre": "Rechaza declaración responsable",
        "descripcion": "Rechaza declaración responsable",
        "emisor": "SISTEMA",
        "tipo": "REHUSE",
    },
    "422": {
        "nombre": "Rechaza parte, transcurrido plazo 72 h. (Traumatismo menor CV)",
        "descripcion": "Rechaza parte, transcurrido plazo 72 h. (Traumatismo menor CV)",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "423": {
        "nombre": "Rechaza parte, lesionado no viaja en espacio destinado a personas",
        "descripcion": "Rechaza parte, lesionado no viaja en espacio destinado a personas",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "442": {
        "nombre": "Rechaza factura, transcurrido plazo 72 h. (Traumatismo menor CV)",
        "descripcion": "Rechaza factura, transcurrido plazo 72 h. (Traumatismo menor CV)",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "443": {
        "nombre": "Rechaza factura, Lesionado no en espacio destinado a personas",
        "descripcion": "Rechaza factura, Lesionado no en espacio destinado a personas",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "471": {
        "nombre": "Rechazo del parte de asistencia",
        "descripcion": "Rechazo del parte de asistencia",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "472": {
        "nombre": "Parte de asistencia no cumplimentado correctamente",
        "descripcion": "Parte de asistencia no cumplimentado correctamente",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "473": {
        "nombre": "No hay acuerdo con el contenido del parte de asistencia",
        "descripcion": "No hay acuerdo con el contenido del parte de asistencia",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "474": {
        "nombre": "Rechaza el parte por no asegurar al vehículo",
        "descripcion": "Rechaza el parte por no asegurar al vehículo",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "475": {
        "nombre": "No corresponde el pago (estipulación de Convenio)",
        "descripcion": "No corresponde el pago (estipulación de Convenio)",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "476": {
        "nombre": "Rechaza parte, no corresponde pago entidad no adherida",
        "descripcion": "Rechaza parte, no corresponde pago entidad no adherida",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "477": {
        "nombre": "Rechaza parte, conductor sin cobertura",
        "descripcion": "Rechaza parte, conductor sin cobertura",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "478": {
        "nombre": "Rechaza por existir seguro",
        "descripcion": "Rechaza por existir seguro",
        "emisor": "SISTEMA",
        "tipo": "REHUSE",
    },
    "481": {
        "nombre": "Rechaza factura",
        "descripcion": "Rechaza factura / Rechaza factura: asistencia posterior a comunicación no aceptación",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "482": {
        "nombre": "Rechaza factura por no asegurar el vehículo",
        "descripcion": "Rechaza factura por no asegurar el vehículo",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "483": {
        "nombre": "Rechaza factura por no aplicar convenio",
        "descripcion": "Rechaza factura por no aplicar convenio",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "484": {
        "nombre": "Rechaza factura por existir seguro",
        "descripcion": "Rechaza factura por existir seguro",
        "emisor": "SISTEMA",
        "tipo": "REHUSE",
    },
    "485": {
        "nombre": "Rechaza factura, no corresponde pago entidad no adherida",
        "descripcion": "Rechaza factura, no corresponde pago entidad no adherida",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "486": {
        "nombre": "Rechazo factura, transcurso de los plazos previstos en el Convenio",
        "descripcion": "Rechazo factura, transcurso de los plazos previstos en el Convenio",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "487": {
        "nombre": "Rechaza Factura, conductor sin cobertura",
        "descripcion": "Rechaza Factura, conductor sin cobertura / discrepancia o desproporción entre diagnóstico y tratamiento",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "488": {
        "nombre": "Rechaza factura, prestación no autorizada",
        "descripcion": "Rechaza factura, prestación no autorizada",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "492": {
        "nombre": "No se trata de un hecho de la circulación",
        "descripcion": "No se trata de un hecho de la circulación",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "494": {
        "nombre": "Transcurso de los plazos previstos en el Convenio",
        "descripcion": "Transcurso de los plazos previstos en el Convenio",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "495": {
        "nombre": "Existencia probada de fraude",
        "descripcion": "Existencia probada de fraude",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "496": {
        "nombre": "Falta de relación causal, criterio cronológico",
        "descripcion": "Falta de relación causal, criterio cronológico",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "497": {
        "nombre": "Falta de relación causal, criterio de intensidad",
        "descripcion": "Falta de relación causal, criterio de intensidad",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "498": {
        "nombre": "Falta de relación causal, criterio topográfico",
        "descripcion": "Falta de relación causal, criterio topográfico",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    "499": {
        "nombre": "Falta de relación causal, criterio de exclusión",
        "descripcion": "Falta de relación causal, criterio de exclusión",
        "emisor": "ASEGURADORA",
        "tipo": "REHUSE",
    },
    # --- Códigos 5xx: Cierre y facturación ---
    "500": {
        "nombre": "Abandona gestión expediente",
        "descripcion": "Abandona gestión expediente",
        "emisor": "HOSPITAL",
        "tipo": "CIERRE",
    },
    "501": {
        "nombre": "Baja de expediente con pago",
        "descripcion": "Baja de expediente con pago",
        "emisor": "HOSPITAL",
        "tipo": "CIERRE",
    },
    "502": {
        "nombre": "Baja del expediente",
        "descripcion": "Baja del expediente",
        "emisor": "SISTEMA",
        "tipo": "CIERRE",
    },
    "503": {
        "nombre": "Acepta rechazo de parte",
        "descripcion": "Acepta rechazo de parte",
        "emisor": "SISTEMA",
        "tipo": "CIERRE",
    },
    "504": {
        "nombre": "Baja expediente no convenio",
        "descripcion": "Baja expediente no convenio",
        "emisor": "HOSPITAL",
        "tipo": "CIERRE",
    },
    "570": {
        "nombre": "Abandona gestión de factura",
        "descripcion": "Abandona gestión de factura",
        "emisor": "SISTEMA",
        "tipo": "CIERRE",
    },
    "572": {
        "nombre": "Subcomisión No procede parte",
        "descripcion": "Subcomisión No procede parte",
        "emisor": "SISTEMA",
        "tipo": "CIERRE",
    },
    "573": {
        "nombre": "Comisión resuelve: No procede factura",
        "descripcion": "Comisión resuelve: No procede factura / Subcomisión resuelve no procede factura",
        "emisor": "SISTEMA",
        "tipo": "CIERRE",
    },
    "574": {
        "nombre": "Subcomisión no procede parte tras recurso",
        "descripcion": "Subcomisión no procede parte tras recurso / No procede reducción de tarifas (2010U)",
        "emisor": "SISTEMA",
        "tipo": "CIERRE",
    },
    "575": {
        "nombre": "Comisión resuelve no procede parte",
        "descripcion": "Comisión resuelve no procede parte",
        "emisor": "SISTEMA",
        "tipo": "CIERRE",
    },
    "576": {
        "nombre": "Comisión resuelve no procede factura",
        "descripcion": "Comisión resuelve no procede factura",
        "emisor": "SISTEMA",
        "tipo": "CIERRE",
    },
    "577": {
        "nombre": "Subcomisión no procede factura tras recurso",
        "descripcion": "Subcomisión no procede factura tras recurso",
        "emisor": "SISTEMA",
        "tipo": "CIERRE",
    },
    "578": {
        "nombre": "Subcomisión resuelve no procede pago total",
        "descripcion": "Subcomisión resuelve no procede pago total",
        "emisor": "SISTEMA",
        "tipo": "CIERRE",
    },
    "579": {
        "nombre": "Comisión resuelve No procede total",
        "descripcion": "Comisión resuelve No procede total",
        "emisor": "SISTEMA",
        "tipo": "CIERRE",
    },
    "580": {
        "nombre": "Envía factura rectificativa de anulación",
        "descripcion": "Envía factura rectificativa de anulación",
        "emisor": "HOSPITAL",
        "tipo": "FACTURACION",
    },
    "581": {
        "nombre": "Confirma factura abonada totalmente",
        "descripcion": "Confirma factura abonada totalmente",
        "emisor": "HOSPITAL",
        "tipo": "FACTURACION",
    },
    "582": {
        "nombre": "Confirma factura abonada parcialmente",
        "descripcion": "Confirma factura abonada parcialmente",
        "emisor": "HOSPITAL",
        "tipo": "FACTURACION",
    },
    "583": {
        "nombre": "Factura sin abono por Convenio",
        "descripcion": "Factura sin abono por Convenio",
        "emisor": "HOSPITAL",
        "tipo": "FACTURACION",
    },
    "584": {
        "nombre": "Cierre factura. No procede",
        "descripcion": "Cierre factura. No procede",
        "emisor": "SISTEMA",
        "tipo": "FACTURACION",
    },
    "585": {
        "nombre": "Envía factura rectificativa de importes",
        "descripcion": "Envía factura rectificativa de importes",
        "emisor": "HOSPITAL",
        "tipo": "FACTURACION",
    },
    "586": {
        "nombre": "Cierre factura. No procede total",
        "descripcion": "Cierre factura. No procede total",
        "emisor": "SISTEMA",
        "tipo": "FACTURACION",
    },
    "587": {
        "nombre": "Cierre factura con embargo",
        "descripcion": "Cierre factura con embargo",
        "emisor": "HOSPITAL",
        "tipo": "FACTURACION",
    },
    # --- Códigos 6xx: Subcomisiones y alegaciones ---
    "652": {
        "nombre": "Alegaciones Subcomisión parte",
        "descripcion": "Alegaciones Subcomisión parte",
        "emisor": "AMBOS",
        "tipo": "SUBCOMISION",
    },
    "653": {
        "nombre": "Alegaciones Subcomisión factura",
        "descripcion": "Alegaciones Subcomisión factura",
        "emisor": "AMBOS",
        "tipo": "SUBCOMISION",
    },
    "655": {
        "nombre": "Alegaciones subcomisión cambio de diagnóstico (2010U)",
        "descripcion": "Alegaciones subcomisión cambio de diagnóstico (2010U)",
        "emisor": "SISTEMA",
        "tipo": "SUBCOMISION",
    },
    "662": {
        "nombre": "Subcomisión automatizada por Parte",
        "descripcion": "Subcomisión automatizada por Parte",
        "emisor": "SISTEMA",
        "tipo": "SUBCOMISION",
    },
    "663": {
        "nombre": "Subcomisión automatizada por Factura",
        "descripcion": "Subcomisión automatizada por Factura",
        "emisor": "SISTEMA",
        "tipo": "SUBCOMISION",
    },
    "664": {
        "nombre": "Envío a subcomisión disconformidad reducción tarifa",
        "descripcion": "Envío a subcomisión disconformidad reducción tarifa",
        "emisor": "HOSPITAL",
        "tipo": "SUBCOMISION",
    },
    "665": {
        "nombre": "Subcomisión automatizada por cambio de diagnóstico (2010U)",
        "descripcion": "Subcomisión automatizada por cambio de diagnóstico (2010U)",
        "emisor": "HOSPITAL",
        "tipo": "SUBCOMISION",
    },
    "666": {
        "nombre": "PA elevado a Comisión",
        "descripcion": "PA elevado a Comisión",
        "emisor": "SISTEMA",
        "tipo": "SUBCOMISION",
    },
    "667": {
        "nombre": "Factura elevada a Comisión",
        "descripcion": "Factura elevada a Comisión",
        "emisor": "SISTEMA",
        "tipo": "SUBCOMISION",
    },
    "669": {
        "nombre": "Subcomisión solicita documentación aclaración parte",
        "descripcion": "Subcomisión solicita documentación aclaración parte",
        "emisor": "SISTEMA",
        "tipo": "SUBCOMISION",
    },
    "670": {
        "nombre": "Interlocutores por Parte",
        "descripcion": "Interlocutores por Parte",
        "emisor": "AMBOS",
        "tipo": "SUBCOMISION",
    },
    "671": {
        "nombre": "Interlocutores por Factura",
        "descripcion": "Interlocutores por Factura",
        "emisor": "AMBOS",
        "tipo": "SUBCOMISION",
    },
    "672": {
        "nombre": "Fin gestión Parte en CAS",
        "descripcion": "Fin gestión Parte en CAS. Gestionar con subcomisión no automatizada",
        "emisor": "SISTEMA",
        "tipo": "SUBCOMISION",
    },
    "673": {
        "nombre": "Fin gestión Factura en CAS",
        "descripcion": "Fin gestión Factura en CAS. Gestionar con subcomisión no automatizada",
        "emisor": "SISTEMA",
        "tipo": "SUBCOMISION",
    },
    "674": {
        "nombre": "Subcomisión por falta de pago",
        "descripcion": "Subcomisión por falta de pago",
        "emisor": "SISTEMA",
        "tipo": "SUBCOMISION",
    },
    "676": {
        "nombre": "CCS Pago pendiente",
        "descripcion": "CCS Pago pendiente",
        "emisor": "SISTEMA",
        "tipo": "SUBCOMISION",
    },
    "677": {
        "nombre": "Comisión solicita documentación aclaración Parte",
        "descripcion": "Comisión solicita documentación aclaración Parte",
        "emisor": "SISTEMA",
        "tipo": "SUBCOMISION",
    },
    "678": {
        "nombre": "Subcomisión solicita documentación aclaración Factura",
        "descripcion": "Subcomisión solicita documentación aclaración Factura",
        "emisor": "SISTEMA",
        "tipo": "SUBCOMISION",
    },
    "679": {
        "nombre": "Comisión solicita documentación aclaración Factura",
        "descripcion": "Comisión solicita documentación aclaración Factura",
        "emisor": "SISTEMA",
        "tipo": "SUBCOMISION",
    },
    "682": {
        "nombre": "Resolución firme subcomisión acepta parte",
        "descripcion": "Resolución firme subcomisión acepta parte",
        "emisor": "SISTEMA",
        "tipo": "SUBCOMISION",
    },
    "683": {
        "nombre": "Resolución firme subcomisión no procede parte",
        "descripcion": "Resolución firme subcomisión no procede parte",
        "emisor": "SISTEMA",
        "tipo": "SUBCOMISION",
    },
    "684": {
        "nombre": "Resolución firme subcomisión acepta factura",
        "descripcion": "Resolución firme subcomisión acepta factura",
        "emisor": "SISTEMA",
        "tipo": "SUBCOMISION",
    },
    "685": {
        "nombre": "Resolución firme subcomisión no procede factura",
        "descripcion": "Resolución firme subcomisión no procede factura",
        "emisor": "SISTEMA",
        "tipo": "SUBCOMISION",
    },
    "686": {
        "nombre": "Interlocutores por paciente alta especialización",
        "descripcion": "Interlocutores por paciente alta especialización",
        "emisor": "AMBOS",
        "tipo": "SUBCOMISION",
    },
    "687": {
        "nombre": "Fin gestión lesionado alta complejidad en CAS",
        "descripcion": "Fin gestión lesionado alta complejidad en CAS. Gestionar con subcomisión no automatizada",
        "emisor": "SISTEMA",
        "tipo": "SUBCOMISION",
    },
    # --- Códigos 7xx: Avisos ---
    "715": {
        "nombre": "Aviso caducidad factura",
        "descripcion": "Aviso caducidad factura",
        "emisor": "SISTEMA",
        "tipo": "AVISOS",
    },
    "716": {
        "nombre": "Aviso envío fuera de plazo informe de evolución",
        "descripcion": "Aviso envío fuera de plazo (15 días naturales) del informe de evolución",
        "emisor": "SISTEMA",
        "tipo": "AVISOS",
    },
    "717": {
        "nombre": "Aviso presentación facturas asistencias prestadas",
        "descripcion": "Aviso presentación de las facturas de las asistencias prestadas por los CS",
        "emisor": "SISTEMA",
        "tipo": "AVISOS",
    },
    # --- Códigos 8xx: Documentación clínica y originales ---
    "801": {
        "nombre": "Solicitud autorización calificación lesionado alta especialización",
        "descripcion": "Solicitud de autorización para calificación de lesionado alta especialización",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "806": {
        "nombre": "Informe cambio diagnóstico",
        "descripcion": "Informe cambio diagnóstico",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "811": {
        "nombre": "Informe médico de evolución",
        "descripcion": "Informe médico de evolución",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "814": {
        "nombre": "Envía documento hoja de firmas",
        "descripcion": "Envía documento hoja de firmas",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "821": {
        "nombre": "Envío declaración de responsable",
        "descripcion": "Envío declaración de responsable",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "822": {
        "nombre": "Envío nueva declaración responsable",
        "descripcion": "Envío nueva declaración responsable",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "823": {
        "nombre": "Autorización Infiltraciones-bloqueos facetarios, nerviosos",
        "descripcion": "Autorización Infiltraciones-bloqueos facetarios, nerviosos",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "824": {
        "nombre": "Autorización ondas de choque radiales",
        "descripcion": "Autorización ondas de choque radiales",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "825": {
        "nombre": "Autorización ondas de choque focales",
        "descripcion": "Autorización ondas de choque focales",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "841": {
        "nombre": "Justificante de rechazo de parte",
        "descripcion": "Justificante de rechazo de parte",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "861": {
        "nombre": "EA justifica aplicar módulo reducido",
        "descripcion": "EA justifica aplicar módulo reducido",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "863": {
        "nombre": "Envía Documentos originales información aclaratoria",
        "descripcion": "Envía Documentos originales información aclaratoria",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "864": {
        "nombre": "Centro sanitario justifica diálogo aplicación módulo reducido",
        "descripcion": "Centro sanitario justifica diálogo aplicación módulo reducido",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "865": {
        "nombre": "Documento original de justificación de envío fuera de plazo",
        "descripcion": "Documento original de justificación de envío fuera de plazo",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "866": {
        "nombre": "Documentación original sin catalogar (CH)",
        "descripcion": "Documentación original sin catalogar",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "867": {
        "nombre": "Documentación original sin catalogar (EA)",
        "descripcion": "Documentación original sin catalogar",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "869": {
        "nombre": "Envía Documentos originales de aclaración factura",
        "descripcion": "Envía Documentos originales de aclaración factura",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "870": {
        "nombre": "Documento justificante rechazo factura",
        "descripcion": "Documento justificante rechazo factura",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "874": {
        "nombre": "Documento original de justificante de no aseguramiento",
        "descripcion": "Documento original de justificante de no aseguramiento",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "876": {
        "nombre": "Envía doc. original aclaración declaración responsable",
        "descripcion": "Envía doc. original aclaración declaración responsable",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "877": {
        "nombre": "Doc. original información alegaciones parte (CH)",
        "descripcion": "Doc. original información alegaciones parte",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "878": {
        "nombre": "Doc. original información alegaciones parte (EA)",
        "descripcion": "Doc. original información alegaciones parte",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "879": {
        "nombre": "Doc. original información alegaciones factura (CH)",
        "descripcion": "Doc. original información alegaciones factura",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "880": {
        "nombre": "Doc. original información alegaciones factura (EA)",
        "descripcion": "Doc. original información alegaciones factura",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "881": {
        "nombre": "Informe de alta de urgencias",
        "descripcion": "Informe de alta de urgencias",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "885": {
        "nombre": "Envío informe de alta",
        "descripcion": "Envío informe de alta",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "890": {
        "nombre": "EA envía doc. aclaraciones PA, solicitud subcomisión",
        "descripcion": "EA envía doc. aclaraciones Parte Asistencia, solicitud subcomisión",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "891": {
        "nombre": "CH envía doc aclaraciones PA, solicitud subcomisión",
        "descripcion": "CH envía doc aclaraciones Parte Asistencia, solicitud subcomisión",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "892": {
        "nombre": "CH envía doc. aclaraciones PA, solicitud Comisión",
        "descripcion": "CH envía doc. aclaraciones Parte Asistencia, solicitud Comisión",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "893": {
        "nombre": "CH envía doc. aclaraciones Factura, solicitud Comisión",
        "descripcion": "CH envía doc. aclaraciones Factura, solicitud Comisión",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "894": {
        "nombre": "EA envía doc. aclaraciones Factura, solicitud Comisión",
        "descripcion": "EA envía doc. aclaraciones Factura, solicitud Comisión",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "895": {
        "nombre": "CH envía doc. aclaraciones Factura, solicitud Comisión",
        "descripcion": "CH envía doc. aclaraciones Factura, solicitud Comisión",
        "emisor": "HOSPITAL",
        "tipo": "DOCUMENTACION",
    },
    "896": {
        "nombre": "Documentación subcomisión/comisión",
        "descripcion": "Documentación subcomisión/comisión",
        "emisor": "SISTEMA",
        "tipo": "DOCUMENTACION",
    },
    "897": {
        "nombre": "Documentación adicional tras petición subcomisión/comisión",
        "descripcion": "Documentación adicional tras petición subcomisión/comisión",
        "emisor": "SISTEMA",
        "tipo": "DOCUMENTACION",
    },
    "898": {
        "nombre": "EA envía doc. aclaraciones PA, solicitud Comisión",
        "descripcion": "EA envía doc. aclaraciones Parte Asistencia, solicitud Comisión",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
    "899": {
        "nombre": "EA envía doc. aclaraciones Factura, solicitud Subcomisión",
        "descripcion": "EA envía doc. aclaraciones Factura, solicitud Subcomisión",
        "emisor": "ASEGURADORA",
        "tipo": "DOCUMENTACION",
    },
}

# Conjunto de TODOS los códigos válidos (para validación rápida)
VALID_CAS_CODES = set(CAS_CODES.keys())


# ============================================================
# MÁQUINA DE ESTADOS - TRANSICIONES VÁLIDAS
# ============================================================
# Clave: código actual → Lista de códigos siguientes válidos

CAS_TRANSITIONS = {
    "INICIO": ["101", "171", "175"],  # Códigos que pueden iniciar un diálogo

    # Desde partes iniciales
    "101": ["201", "271", "471", "472"],
    "171": ["271", "471", "472", "475", "476", "477"],
    "175": ["271", "471", "472", "475", "476", "477"],

    # Desde aceptación
    "201": ["301", "311", "362", "500", "501"],
    "271": ["301", "311", "362", "500", "501"],

    # Desde comunicación de continuación
    "301": ["202", "311", "362", "471", "500", "501"],

    # Desde facturación
    "181": ["281", "481", "482", "483", "485", "486", "487", "488"],
    "500": [],
    "501": [],

    # Desde aceptación de factura
    "281": ["381", "500", "501"],

    # Desde rechazos
    "471": ["500", "501", "652"],
    "472": ["172", "500"],
    "481": ["308", "309", "500", "580", "585"],

    # Subcomisiones
    "652": ["270", "572"],
    "662": ["270", "572"],

    # Cierre - no hay transición posible
    "500": [],
    "501": [],
    "502": [],
}

# ============================================================
# TIPOS DE CONVENIO
# ============================================================

CONVENIO_TIPOS = {
    "PUBLICO": {
        "nombre": "Convenio Sanitario Público",
        "codigo_inicio": ["101", "171"],
        "descripcion": "Convenio entre entidades aseguradoras y servicios de salud públicos.",
    },
    "PRIVADO": {
        "nombre": "Convenio Clínicas Privadas",
        "codigo_inicio": ["101", "171"],
        "descripcion": "Convenio entre entidades aseguradoras y clínicas privadas.",
    },
    "EMERGENCIAS": {
        "nombre": "Convenio de Emergencias",
        "codigo_inicio": ["101"],
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

    actions = {
        "INICIO": "Recibido parte inicial. Verificar datos y responder con código 271 (aceptar), 471 (rechazar parte), 472 (parte incorrecto) u otro código de rechazo según normativa.",
        "DOCUMENTACION": "Documentación recibida. Revisar contenido y responder según normativa.",
        "FACTURACION": "Factura recibida. Revisar importes contra baremos y responder con 281 (aceptar), 481 (rechazar) u otro código de rechazo según normativa.",
        "REHUSE": "Rehúse recibido. Registrar motivo y cerrar expediente si procede.",
        "CIERRE": "Expediente cerrado. No requiere acción adicional.",
    }

    return actions.get(tipo, f"Código {code} recibido. Consultar normativa para determinar acción.")
