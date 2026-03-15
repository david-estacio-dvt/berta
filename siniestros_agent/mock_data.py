"""
mock_data.py - Base de datos simulada para el agente CAS.

Contiene datos simulados de pólizas, asegurados, hospitales adheridos y
siniestros. Los expedientes de prueba se basan en los nombres de ficheros
reales de la carpeta amv-documentacion-cas-prueba.
"""

from datetime import datetime, timedelta

# ============================================================
# HOSPITALES ADHERIDOS AL CONVENIO CAS
# ============================================================

HOSPITALES_ADHERIDOS = {
    "HOSP_001": {
        "nombre": "Hospital General Universitario",
        "tipo": "PUBLICO",
        "convenio": "PUBLICO",
        "adherido_desde": "2020-01-01",
        "provincia": "Madrid",
        "activo": True,
    },
    "HOSP_002": {
        "nombre": "Hospital San Rafael",
        "tipo": "PUBLICO",
        "convenio": "PUBLICO",
        "adherido_desde": "2019-06-15",
        "provincia": "Barcelona",
        "activo": True,
    },
    "HOSP_003": {
        "nombre": "Clínica San José",
        "tipo": "PRIVADO",
        "convenio": "PRIVADO",
        "adherido_desde": "2021-03-01",
        "provincia": "Valencia",
        "activo": True,
    },
    "HOSP_004": {
        "nombre": "Hospital Virgen del Rocío",
        "tipo": "PUBLICO",
        "convenio": "PUBLICO",
        "adherido_desde": "2018-01-01",
        "provincia": "Sevilla",
        "activo": True,
    },
    "HOSP_005": {
        "nombre": "Clínica La Milagrosa",
        "tipo": "PRIVADO",
        "convenio": "PRIVADO",
        "adherido_desde": "2022-09-01",
        "provincia": "Madrid",
        "activo": False,  # Ya no está adherida
    },
    "HOSP_GENERAL": {
        "nombre": "Hospital General de Pruebas",
        "tipo": "PUBLICO",
        "convenio": "PUBLICO",
        "adherido_desde": "2020-01-01",
        "provincia": "Madrid",
        "activo": True,
    },
}

# ============================================================
# PÓLIZAS Y ASEGURADOS
# ============================================================

POLIZAS = {
    "POL-2024-001": {
        "titular": "Juan García López",
        "dni": "12345678A",
        "matricula": "1234ABC",
        "vehiculo": "Seat León 2020",
        "fecha_inicio": "2024-01-01",
        "fecha_fin": "2025-01-01",
        "cobertura_sanitaria": True,
        "tipo_cobertura": "Todo riesgo",
        "estado": "VIGENTE",
    },
    "POL-2024-002": {
        "titular": "María Fernández Ruiz",
        "dni": "87654321B",
        "matricula": "5678DEF",
        "vehiculo": "Volkswagen Golf 2022",
        "fecha_inicio": "2024-03-15",
        "fecha_fin": "2025-03-15",
        "cobertura_sanitaria": True,
        "tipo_cobertura": "Terceros ampliado",
        "estado": "VIGENTE",
    },
    "POL-2024-003": {
        "titular": "Pedro Martínez Sánchez",
        "dni": "11223344C",
        "matricula": "9012GHI",
        "vehiculo": "Ford Focus 2019",
        "fecha_inicio": "2024-06-01",
        "fecha_fin": "2025-06-01",
        "cobertura_sanitaria": True,
        "tipo_cobertura": "Terceros básico",
        "estado": "VIGENTE",
    },
    "POL-2023-EXPIRED": {
        "titular": "Ana López Díaz",
        "dni": "55667788D",
        "matricula": "3456JKL",
        "vehiculo": "Renault Clio 2018",
        "fecha_inicio": "2023-01-01",
        "fecha_fin": "2024-01-01",
        "cobertura_sanitaria": True,
        "tipo_cobertura": "Terceros",
        "estado": "EXPIRADA",
    },
    "POLIZA_ACTIVA": {
        "titular": "Test Asegurado Activo",
        "dni": "99887766E",
        "matricula": "TEST123",
        "vehiculo": "Test Car 2024",
        "fecha_inicio": "2024-01-01",
        "fecha_fin": "2026-12-31",
        "cobertura_sanitaria": True,
        "tipo_cobertura": "Todo riesgo",
        "estado": "VIGENTE",
    },
}

# ============================================================
# SINIESTROS / ACCIDENTES
# ============================================================

SINIESTROS = {
    "SIN-2024-001": {
        "fecha_ocurrencia": "2024-11-15",
        "tipo": "Colisión trasera",
        "lugar": "Madrid - Calle Gran Vía",
        "vehiculos_implicados": ["1234ABC", "XXXX999"],
        "lesionados": [
            {"nombre": "Juan García López", "dni": "12345678A", "posicion": "Conductor", "lesion": "Cervicalgia"}
        ],
        "poliza": "POL-2024-001",
        "estado": "ABIERTO",
        "notas": [],
    },
    "SIN-2024-002": {
        "fecha_ocurrencia": "2024-12-01",
        "tipo": "Colisión lateral",
        "lugar": "Barcelona - Diagonal",
        "vehiculos_implicados": ["5678DEF", "YYYY888"],
        "lesionados": [
            {"nombre": "María Fernández Ruiz", "dni": "87654321B", "posicion": "Conductora", "lesion": "Contusión múltiple"}
        ],
        "poliza": "POL-2024-002",
        "estado": "ABIERTO",
        "notas": [],
    },
    "SIN-2025-001": {
        "fecha_ocurrencia": "2025-01-20",
        "tipo": "Alcance trasero",
        "lugar": "Valencia - Autopista V-30",
        "vehiculos_implicados": ["9012GHI", "ZZZZ777"],
        "lesionados": [
            {"nombre": "Pedro Martínez Sánchez", "dni": "11223344C", "posicion": "Conductor", "lesion": "Latigazo cervical"},
            {"nombre": "Laura Martínez", "dni": "44332211F", "posicion": "Acompañante", "lesion": "Contusión dorsal"}
        ],
        "poliza": "POL-2024-003",
        "estado": "ABIERTO",
        "notas": [],
    },
    "VALID_ACCIDENT": {
        "fecha_ocurrencia": "2025-01-01",
        "tipo": "Alcance trasero (test)",
        "lugar": "Test Location",
        "vehiculos_implicados": ["TEST123"],
        "lesionados": [
            {"nombre": "Test Asegurado Activo", "dni": "99887766E", "posicion": "Conductor", "lesion": "Cervicalgia"}
        ],
        "poliza": "POLIZA_ACTIVA",
        "estado": "ABIERTO",
        "notas": [],
    },
}

# ============================================================
# EXPEDIENTES CAS (basados en ficheros de prueba reales)
# ============================================================
# Los números de expediente se basan en los nombres de fichero
# de la carpeta amv-documentacion-cas-prueba

EXPEDIENTES_CAS = {
    "202400785782": {
        "siniestro": "SIN-2024-001",
        "hospital": "HOSP_001",
        "convenio": "PUBLICO",
        "estado_cas": "EN_TRAMITACION",
        "ultimo_codigo": "100",
        "historial_codigos": ["100"],
        "documentos": ["202400785782-97446073-001.pdf", "202400785782-97446073-002.pdf"],
        "fecha_apertura": "2024-11-16",
        "importe_reclamado": None,
        "importe_aceptado": None,
    },
    "202400926113": {
        "siniestro": "SIN-2024-002",
        "hospital": "HOSP_002",
        "convenio": "PUBLICO",
        "estado_cas": "ACEPTADO",
        "ultimo_codigo": "400",
        "historial_codigos": ["100", "200", "328", "400"],
        "documentos": ["202400926113-99147021-001.pdf"],
        "fecha_apertura": "2024-12-02",
        "importe_reclamado": None,
        "importe_aceptado": None,
    },
    "202500105110": {
        "siniestro": "SIN-2025-001",
        "hospital": "HOSP_003",
        "convenio": "PRIVADO",
        "estado_cas": "DOCUMENTACION",
        "ultimo_codigo": "328",
        "historial_codigos": ["100", "200", "301", "328"],
        "documentos": [
            "202500105110-99598557-001.PDF",
            "202500105110-99598563-001.JPEG",
            "202500105110-99598569-001.JPEG",
            "202500105110-99598576-001.JPEG",
            "202500105110-99598581-001.JPEG",
            "202500105110-99598588-001.JPEG",
            "202500105110-99598594-001.JPEG",
            "202500105110-99598604-001.JPEG",
            "202500105110-99598608-001.PDF",
            "202500105110-99636657-001.JPG",
        ],
        "fecha_apertura": "2025-01-21",
        "importe_reclamado": 2450.00,
        "importe_aceptado": None,
    },
    "202500277090": {
        "siniestro": "SIN-2025-001",
        "hospital": "HOSP_004",
        "convenio": "PUBLICO",
        "estado_cas": "EN_TRAMITACION",
        "ultimo_codigo": "200",
        "historial_codigos": ["100", "200"],
        "documentos": ["202500277090-101129922-001.pdf", "202500277090-103361758-001.pdf"],
        "fecha_apertura": "2025-01-25",
        "importe_reclamado": None,
        "importe_aceptado": None,
    },
    "202500399716": {
        "siniestro": "SIN-2024-001",
        "hospital": "HOSP_001",
        "convenio": "PUBLICO",
        "estado_cas": "DOCUMENTACION",
        "ultimo_codigo": "301",
        "historial_codigos": ["100", "300", "301"],
        "documentos": [
            "202500399716-102175214-001.PDF",
            "202500399716-102569328-001.pdf",
            "202500399716-102772724-001.PDF",
        ],
        "fecha_apertura": "2025-02-01",
        "importe_reclamado": None,
        "importe_aceptado": None,
    },
}

# ============================================================
# BAREMOS Y TARIFAS CAS
# ============================================================

BAREMOS_CAS = {
    "PUBLICO": {
        "consulta_urgencias": {"max": 150.00, "descripcion": "Consulta de urgencias"},
        "consulta_especialista": {"max": 80.00, "descripcion": "Consulta especialista"},
        "radiografia": {"max": 45.00, "descripcion": "Radiografía simple"},
        "tac": {"max": 250.00, "descripcion": "TAC craneal o cervical"},
        "resonancia": {"max": 350.00, "descripcion": "Resonancia magnética"},
        "collarín": {"max": 25.00, "descripcion": "Collarín cervical"},
        "rehabilitacion_sesion": {"max": 35.00, "descripcion": "Sesión de rehabilitación"},
        "dia_hospitalizacion": {"max": 450.00, "descripcion": "Día de hospitalización"},
        "cirugia_menor": {"max": 800.00, "descripcion": "Cirugía menor"},
        "cirugia_mayor": {"max": 5000.00, "descripcion": "Cirugía mayor"},
        "ambulancia": {"max": 200.00, "descripcion": "Servicio de ambulancia"},
    },
    "PRIVADO": {
        "consulta_urgencias": {"max": 200.00, "descripcion": "Consulta de urgencias"},
        "consulta_especialista": {"max": 120.00, "descripcion": "Consulta especialista"},
        "radiografia": {"max": 60.00, "descripcion": "Radiografía simple"},
        "tac": {"max": 350.00, "descripcion": "TAC craneal o cervical"},
        "resonancia": {"max": 500.00, "descripcion": "Resonancia magnética"},
        "collarín": {"max": 30.00, "descripcion": "Collarín cervical"},
        "rehabilitacion_sesion": {"max": 50.00, "descripcion": "Sesión de rehabilitación"},
        "dia_hospitalizacion": {"max": 600.00, "descripcion": "Día de hospitalización"},
        "cirugia_menor": {"max": 1200.00, "descripcion": "Cirugía menor"},
        "cirugia_mayor": {"max": 8000.00, "descripcion": "Cirugía mayor"},
        "ambulancia": {"max": 300.00, "descripcion": "Servicio de ambulancia"},
    },
}

# ============================================================
# FUNCIONES DE BÚSQUEDA
# ============================================================

def find_policy_by_matricula(matricula: str) -> dict | None:
    """Busca una póliza por matrícula de vehículo."""
    for pol_id, pol in POLIZAS.items():
        if pol["matricula"].upper() == matricula.upper():
            result = pol.copy()
            result["id"] = pol_id
            return result
    return None


def find_policy_by_dni(dni: str) -> dict | None:
    """Busca una póliza por DNI del titular."""
    for pol_id, pol in POLIZAS.items():
        if pol["dni"].upper() == dni.upper():
            result = pol.copy()
            result["id"] = pol_id
            return result
    return None


def find_siniestro(siniestro_id: str) -> dict | None:
    """Busca un siniestro por ID."""
    return SINIESTROS.get(siniestro_id)


def find_expediente(expediente_id: str) -> dict | None:
    """Busca un expediente CAS por número."""
    return EXPEDIENTES_CAS.get(expediente_id)


def find_hospital(hospital_id: str) -> dict | None:
    """Busca un hospital en el registro de adhesiones."""
    return HOSPITALES_ADHERIDOS.get(hospital_id)
