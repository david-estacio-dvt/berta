"""
schemas.py - Modelos Pydantic para la API REST de Berta CAS.

Define los formatos de entrada (ParteInput) y salida (BertaResponse)
para la integración con el sistema de IT.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────
# ENUMS
# ─────────────────────────────────────────────

class EstadoCola(str, Enum):
    PROCESADO_AUTO = "PROCESADO_AUTOMATICAMENTE"
    PENDIENTE_VALIDACION = "PENDIENTE_VALIDACION"
    REQUIERE_INTERVENCION = "REQUIERE_INTERVENCION_MANUAL"


class NivelConfianza(str, Enum):
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAJA = "BAJA"


class DecisionBerta(str, Enum):
    ACEPTAR = "ACEPTAR"
    ACEPTAR_RESERVAS = "ACEPTAR_CON_RESERVAS"
    SOLICITAR_DOC = "SOLICITAR_DOCUMENTACION"
    REHUSAR = "REHUSAR"
    PENDIENTE = "PENDIENTE_INFO"


class EstadoValidacion(str, Enum):
    PENDIENTE = "PENDIENTE"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"
    MODIFICADO = "MODIFICADO"


# ─────────────────────────────────────────────
# REQUEST — Lo que envía el sistema de IT
# ─────────────────────────────────────────────

class DocumentoAdjunto(BaseModel):
    nombre_archivo: str = Field(..., description="Nombre del fichero adjunto")
    tipo: Optional[str] = Field(None, description="Tipo MIME o extensión: pdf, jpg, xml")
    descripcion: Optional[str] = Field(None, description="Descripción del documento: 'Informe urgencias'")


class ParteInput(BaseModel):
    """
    Payload que el sistema de IT envía a Berta para cada parte CAS.
    """
    # Identificación del expediente
    expediente_id: str = Field(..., description="ID del expediente CAS. Ej: 202600086262")
    codigo_cas: str = Field(..., description="Código CAS del mensaje. Ej: '100', '328', '500'")
    convenio_tipo: Optional[str] = Field("PUBLICO", description="Tipo de convenio: PUBLICO, PRIVADO, EMERGENCIAS")

    # Datos del hospital
    hospital_id: str = Field(..., description="ID del hospital. Ej: 'HOSP_001'")
    hospital_nombre: Optional[str] = Field(None, description="Nombre del hospital para contexto")

    # Datos del siniestro/accidente
    siniestro_id: Optional[str] = Field(None, description="ID del siniestro. Ej: 'SIN-2024-001'")
    fecha_ocurrencia: Optional[str] = Field(None, description="Fecha del accidente. Formato: YYYY-MM-DD")
    tipo_accidente: Optional[str] = Field(None, description="Descripción del tipo de accidente")

    # Datos del vehículo
    matricula_asegurado: Optional[str] = Field(None, description="Matrícula del vehículo asegurado. Ej: '1234ABC'")
    matricula_contrario: Optional[str] = Field(None, description="Matrícula del vehículo contrario (si aplica)")

    # Datos del lesionado
    lesionado_nombre: Optional[str] = Field(None, description="Nombre completo del lesionado")
    lesionado_dni: Optional[str] = Field(None, description="DNI del lesionado. Ej: '12345678A'")
    lesionado_posicion: Optional[str] = Field(None, description="Posición en el vehículo: Conductor, Copiloto, Pasajero")
    lesion_declarada: Optional[str] = Field(None, description="Descripción de la lesión. Ej: 'Cervicalgia postraumática'")

    # Facturación (si aplica)
    importe_reclamado: Optional[float] = Field(None, description="Importe de la factura en euros (solo para código 500/501)")
    servicios_facturados: Optional[List[dict]] = Field(None, description="Lista de servicios: [{codigo, descripcion, cantidad, precio_unitario}]")

    # Documentación adjunta
    documentos: Optional[List[DocumentoAdjunto]] = Field(default_factory=list, description="Lista de documentos adjuntos")

    # Contexto adicional
    notas_hospital: Optional[str] = Field(None, description="Notas libres del hospital sobre el caso")
    timestamp_envio: Optional[datetime] = Field(None, description="Timestamp del envío por parte del hospital")

    class Config:
        json_schema_extra = {
            "example": {
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
        }


# ─────────────────────────────────────────────
# RESPONSE — Lo que devuelve Berta
# ─────────────────────────────────────────────

class VerificacionDetalle(BaseModel):
    nombre: str
    resultado: str  # "OK", "FALLO", "ALERTA", "INFO"
    detalle: str


class BertaResponse(BaseModel):
    """
    Respuesta estructurada de Berta. Se almacena en la cola para validación humana.
    """
    # Trazabilidad
    expediente_id: str
    codigo_cas_recibido: str
    timestamp_analisis: datetime = Field(default_factory=datetime.utcnow)
    id_analisis: str  # UUID único de este análisis

    # Decisión
    decision: DecisionBerta
    codigo_cas_respuesta: Optional[str] = Field(None, description="Código CAS que Berta propone emitir")
    confianza: NivelConfianza

    # Cola de validación
    estado_cola: EstadoCola
    requiere_accion_humana: bool

    # Análisis completo
    resumen_caso: str
    verificaciones: List[VerificacionDetalle]
    justificacion_normativa: str
    alertas: List[str] = Field(default_factory=list)

    # Nota para el expediente (lista para pegar)
    nota_expediente: str

    # Respuesta completa de Berta (texto libre para log)
    respuesta_completa: str


class ValidacionHumana(BaseModel):
    """
    Payload que el tramitador humano envía al validar/rechazar la propuesta de Berta.
    """
    validacion: EstadoValidacion
    tramitador_id: str = Field(..., description="ID del tramitador que valida")
    notas_tramitador: Optional[str] = Field(None, description="Comentarios del tramitador")
    codigo_cas_final: Optional[str] = Field(None, description="Código CAS final si el tramitador lo modifica")


class ItemCola(BaseModel):
    """Elemento de la cola de validación."""
    id_analisis: str
    expediente_id: str
    codigo_cas: str
    decision_berta: DecisionBerta
    confianza: NivelConfianza
    estado_cola: EstadoCola
    estado_validacion: EstadoValidacion
    timestamp_analisis: datetime
    timestamp_validacion: Optional[datetime] = None
    tramitador_id: Optional[str] = None


# ─────────────────────────────────────────────
# SIAX / ServiciosGemini
# ─────────────────────────────────────────────

class ContextoAMV(BaseModel):
    """
    Datos del sistema interno de AMV que se pasan a Berta para cruzar
    con los datos de SIAX. Si se proporcionan, Berta los usará para
    verificar póliza, matrícula, posición del lesionado, etc.
    """
    expediente_id: Optional[str] = Field(None, description="ID del expediente interno AMV")
    siniestro_id: Optional[str] = Field(None, description="ID del siniestro en AMV. Ej: 'SIN-2024-001'")
    matricula_asegurado: Optional[str] = Field(None, description="Matrícula del vehículo de nuestro asegurado")
    matricula_contrario: Optional[str] = Field(None, description="Matrícula del vehículo contrario")
    dni_lesionado: Optional[str] = Field(None, description="DNI del lesionado")
    nombre_lesionado: Optional[str] = Field(None, description="Nombre del lesionado")
    posicion_lesionado: Optional[str] = Field(None, description="Posición en vehículo: Conductor, Copiloto, Pasajero, etc.")
    fecha_ocurrencia: Optional[str] = Field(None, description="Fecha del accidente (YYYY-MM-DD)")
    siniestro_confirmado: Optional[bool] = Field(None, description="¿El tramitador ha confirmado el siniestro?")
    notas_tramitador: Optional[str] = Field(None, description="Notas del tramitador de corporal")
    ambulancia: Optional[bool] = Field(None, description="¿Acudió ambulancia al siniestro?")


class SiaxAnalisisCasoRequest(BaseModel):
    """Request para analizar todas las conversaciones de un caso CAS (Botón 1)."""
    id_cas: int = Field(..., description="ID de la reclamación CAS en SIAX", examples=[15])
    contexto_amv: Optional[ContextoAMV] = Field(
        None,
        description="Datos internos de AMV para cruzar con SIAX. "
                    "Si se proporcionan, Berta verificará póliza, matrícula, "
                    "posición del lesionado y confirmación del siniestro."
    )


class SiaxAnalisisMensajeRequest(BaseModel):
    """Request para analizar un mensaje específico y recomendar respuesta (Botón 2)."""
    id_cas: int = Field(..., description="ID de la reclamación CAS en SIAX", examples=[15])
    id_mensaje: int = Field(..., description="ID del mensaje específico a analizar", examples=[50])
    contexto_amv: Optional[ContextoAMV] = Field(
        None,
        description="Datos internos de AMV para cruzar con SIAX. "
                    "Si se proporcionan, Berta verificará póliza, matrícula, "
                    "posición del lesionado y confirmación del siniestro."
    )


class MensajeCasSiax(BaseModel):
    """Un mensaje CAS dentro de una secuencia, enriquecido con análisis."""
    id: int
    codigo: str
    nombre: Optional[str] = None
    emisor: str = Field(description="HOSPITAL o ASEGURADORA")
    estado: str
    convenio_normas: Optional[str] = None
    fecha_caducidad: Optional[str] = None
    caducado: bool = False
    puede_responder: bool = False
    mensaje_referido: Optional[int] = None
    codigos_respuesta_validos: List[str] = Field(default_factory=list)


class SecuenciaCasSiax(BaseModel):
    """Una secuencia CAS con sus mensajes."""
    referencia_cas: str
    total_mensajes: int
    ultimo_codigo: Optional[str] = None
    necesita_accion: bool = False
    mensajes: List[MensajeCasSiax] = Field(default_factory=list)


class SiaxAnalisisResponse(BaseModel):
    """Respuesta del análisis SIAX, incluye datos + análisis de Berta."""
    id_cas: int
    total_secuencias: int = 0
    total_mensajes: int = 0
    secuencias_respondibles: int = 0
    secuencias: List[SecuenciaCasSiax] = Field(default_factory=list)
    analisis_berta: Optional[str] = Field(None, description="Análisis completo de Berta en texto libre")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
