"""
tools.py - Herramientas del Agente CAS "Berta".

Funciones que el agente puede invocar para verificar datos contra sistemas
internos (simulados), parsear mensajes CAS y leer documentación adjunta.
"""

import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timedelta

try:
    from .cas_codes import (
        CAS_CODES, CAS_TRANSITIONS, MOTIVOS_REHUSE,
        validate_transition, get_code_info, get_required_action
    )
    from .mock_data import (
        find_policy_by_matricula, find_policy_by_dni,
        find_siniestro, find_expediente, find_hospital,
        BAREMOS_CAS, EXPEDIENTES_CAS, POLIZAS, SINIESTROS
    )
except ImportError:
    from cas_codes import (
        CAS_CODES, CAS_TRANSITIONS, MOTIVOS_REHUSE,
        validate_transition, get_code_info, get_required_action
    )
    from mock_data import (
        find_policy_by_matricula, find_policy_by_dni,
        find_siniestro, find_expediente, find_hospital,
        BAREMOS_CAS, EXPEDIENTES_CAS, POLIZAS, SINIESTROS
    )

DOCS_DIR = Path(__file__).parent / ".documentation"
TEST_CASES_DIR = DOCS_DIR / "amv-documentacion-cas-prueba"


# ============================================================
# 1. VERIFICACIÓN DE PERSONAS Y VEHÍCULOS
# ============================================================

def verify_injured_person(dni: str = "", matricula: str = "", nombre: str = "") -> str:
    """
    Verifica si el lesionado existe en la base de datos de asegurados.
    Busca por DNI, matrícula del vehículo o nombre.
    
    Args:
        dni: DNI/NIF del lesionado
        matricula: Matrícula del vehículo implicado
        nombre: Nombre del lesionado
    
    Returns:
        Resultado de la verificación con datos del asegurado si existe.
    """
    result = None
    
    if dni:
        result = find_policy_by_dni(dni)
    elif matricula:
        result = find_policy_by_matricula(matricula)
    
    if result:
        return json.dumps({
            "estado": "VERIFICADO",
            "titular": result["titular"],
            "dni": result["dni"],
            "matricula": result["matricula"],
            "vehiculo": result["vehiculo"],
            "poliza_id": result["id"],
            "poliza_estado": result["estado"],
            "cobertura_sanitaria": result["cobertura_sanitaria"],
        }, ensure_ascii=False)
    
    if not dni and not matricula and not nombre:
        return json.dumps({
            "estado": "ERROR",
            "mensaje": "Debe proporcionar al menos DNI, matrícula o nombre para buscar al lesionado."
        }, ensure_ascii=False)
    
    return json.dumps({
        "estado": "NO_ENCONTRADO",
        "mensaje": f"No se encontró asegurado con los datos proporcionados (DNI: {dni}, Matrícula: {matricula}, Nombre: {nombre}). Verificar datos o considerar rehúse R02.",
        "accion_recomendada": "Solicitar más información al hospital o rehusar si no hay cobertura."
    }, ensure_ascii=False)


# ============================================================
# 2. VERIFICACIÓN DE PÓLIZA Y COBERTURA
# ============================================================

def verify_insurance_policy(matricula: str = "", dni: str = "", fecha_ocurrencia: str = "") -> str:
    """
    Verifica la vigencia de una póliza en la fecha del siniestro.
    
    Args:
        matricula: Matrícula del vehículo asegurado
        dni: DNI del titular de la póliza
        fecha_ocurrencia: Fecha del accidente (YYYY-MM-DD)
    
    Returns:
        Resultado de verificación de vigencia y cobertura sanitaria.
    """
    policy = None
    if matricula:
        policy = find_policy_by_matricula(matricula)
    elif dni:
        policy = find_policy_by_dni(dni)
    
    if not policy:
        return json.dumps({
            "estado": "NO_ENCONTRADA",
            "mensaje": "Póliza no encontrada. Posible motivo de rehúse R01/R02.",
            "motivo_rehuse": "R02"
        }, ensure_ascii=False)
    
    # Verificar estado
    if policy["estado"] == "EXPIRADA":
        return json.dumps({
            "estado": "EXPIRADA",
            "poliza_id": policy["id"],
            "titular": policy["titular"],
            "fecha_fin": policy["fecha_fin"],
            "mensaje": "Póliza EXPIRADA. No hay cobertura vigente.",
            "motivo_rehuse": "R01"
        }, ensure_ascii=False)
    
    # Verificar fecha de ocurrencia dentro de vigencia
    if fecha_ocurrencia:
        try:
            fecha = datetime.strptime(fecha_ocurrencia, "%Y-%m-%d")
            inicio = datetime.strptime(policy["fecha_inicio"], "%Y-%m-%d")
            fin = datetime.strptime(policy["fecha_fin"], "%Y-%m-%d")
            
            if not (inicio <= fecha <= fin):
                return json.dumps({
                    "estado": "FUERA_VIGENCIA",
                    "poliza_id": policy["id"],
                    "vigencia": f"{policy['fecha_inicio']} a {policy['fecha_fin']}",
                    "fecha_ocurrencia": fecha_ocurrencia,
                    "mensaje": "La fecha del siniestro está FUERA del período de vigencia de la póliza.",
                    "motivo_rehuse": "R01"
                }, ensure_ascii=False)
        except ValueError:
            pass
    
    # Verificar cobertura sanitaria
    if not policy.get("cobertura_sanitaria"):
        return json.dumps({
            "estado": "SIN_COBERTURA_SANITARIA",
            "poliza_id": policy["id"],
            "mensaje": "Póliza vigente pero SIN cobertura sanitaria CAS.",
        }, ensure_ascii=False)
    
    return json.dumps({
        "estado": "VIGENTE",
        "poliza_id": policy["id"],
        "titular": policy["titular"],
        "tipo_cobertura": policy["tipo_cobertura"],
        "vigencia": f"{policy['fecha_inicio']} a {policy['fecha_fin']}",
        "cobertura_sanitaria": True,
        "mensaje": "Póliza VIGENTE con cobertura sanitaria activa."
    }, ensure_ascii=False)


# ============================================================
# 3. VERIFICACIÓN DE SINIESTRO / ACCIDENTE
# ============================================================

def verify_accident(accident_id: str = "", matricula: str = "", fecha_ocurrencia: str = "") -> str:
    """
    Comprueba que el siniestro existe y que los datos son coherentes.
    
    Args:
        accident_id: ID del siniestro
        matricula: Matrícula del vehículo implicado
        fecha_ocurrencia: Fecha declarada del accidente
    
    Returns:
        Datos del siniestro si existe y es coherente.
    """
    siniestro = find_siniestro(accident_id) if accident_id else None
    
    if not siniestro:
        # Intentar buscar por matrícula
        if matricula:
            for sin_id, sin in SINIESTROS.items():
                if matricula.upper() in [v.upper() for v in sin.get("vehiculos_implicados", [])]:
                    siniestro = sin
                    accident_id = sin_id
                    break
    
    if not siniestro:
        return json.dumps({
            "estado": "NO_ENCONTRADO",
            "mensaje": f"Siniestro '{accident_id}' no encontrado en el sistema. Verificar datos o posible rehúse R10.",
            "motivo_rehuse": "R10"
        }, ensure_ascii=False)
    
    # Verificar coherencia de fecha
    if fecha_ocurrencia and siniestro.get("fecha_ocurrencia") != fecha_ocurrencia:
        return json.dumps({
            "estado": "INCOHERENCIA_FECHA",
            "siniestro_id": accident_id,
            "fecha_sistema": siniestro["fecha_ocurrencia"],
            "fecha_declarada": fecha_ocurrencia,
            "mensaje": "ALERTA: La fecha declarada NO coincide con la registrada en el sistema.",
            "accion_recomendada": "Verificar con el hospital la fecha correcta antes de proceder."
        }, ensure_ascii=False)
    
    return json.dumps({
        "estado": "VERIFICADO",
        "siniestro_id": accident_id,
        "fecha_ocurrencia": siniestro["fecha_ocurrencia"],
        "tipo": siniestro["tipo"],
        "lugar": siniestro["lugar"],
        "vehiculos": siniestro["vehiculos_implicados"],
        "lesionados": [
            {
                "nombre": l["nombre"],
                "dni": l["dni"],
                "posicion": l["posicion"],
                "lesion": l["lesion"]
            } for l in siniestro.get("lesionados", [])
        ],
        "estado_siniestro": siniestro["estado"],
        "poliza": siniestro.get("poliza"),
        "mensaje": "Siniestro encontrado y verificado."
    }, ensure_ascii=False)


# ============================================================
# 4. VALIDACIÓN DE SECUENCIA DE CÓDIGOS CAS
# ============================================================

def check_cas_code_sequence(expediente_id: str, nuevo_codigo: str) -> str:
    """
    Valida que el nuevo código CAS sea válido según el estado actual del expediente.
    Implementa la máquina de estados del protocolo CAS.
    
    Args:
        expediente_id: Número de expediente CAS
        nuevo_codigo: Código CAS que se quiere enviar/procesar
    
    Returns:
        Resultado de la validación con la acción recomendada.
    """
    expediente = find_expediente(expediente_id)
    
    if not expediente:
        # Nuevo expediente - verificar que es un código de inicio
        if nuevo_codigo in CAS_TRANSITIONS.get("INICIO", []):
            code_info = get_code_info(nuevo_codigo)
            return json.dumps({
                "estado": "VALIDO_INICIO",
                "codigo": nuevo_codigo,
                "nombre": code_info.get("nombre"),
                "mensaje": f"Código {nuevo_codigo} es válido como inicio de diálogo CAS.",
                "datos_obligatorios": code_info.get("datos_obligatorios", []),
                "plazo_respuesta_dias": code_info.get("plazo_respuesta_dias"),
                "accion_recomendada": get_required_action(nuevo_codigo)
            }, ensure_ascii=False)
        else:
            return json.dumps({
                "estado": "INVALIDO",
                "mensaje": f"Código {nuevo_codigo} NO puede iniciar un diálogo CAS. Códigos válidos de inicio: {CAS_TRANSITIONS['INICIO']}",
            }, ensure_ascii=False)
    
    # Expediente existente - validar transición
    ultimo_codigo = expediente["ultimo_codigo"]
    result = validate_transition(ultimo_codigo, nuevo_codigo)
    
    code_info = get_code_info(nuevo_codigo)
    
    return json.dumps({
        "estado": "VALIDO" if result["valid"] else "INVALIDO",
        "expediente": expediente_id,
        "codigo_actual": ultimo_codigo,
        "codigo_propuesto": nuevo_codigo,
        "nombre_codigo": code_info.get("nombre", "Desconocido"),
        "historial": expediente.get("historial_codigos", []),
        "transicion_valida": result["valid"],
        "mensaje": result["message"],
        "codigos_permitidos": result["allowed_codes"],
        "accion_recomendada": get_required_action(nuevo_codigo) if result["valid"] else "Seleccionar un código válido de la lista permitida."
    }, ensure_ascii=False)


# ============================================================
# 5. VERIFICACIÓN DE HOSPITAL ADHERIDO
# ============================================================

def check_hospital_adhesion(hospital_id: str, convenio_tipo: str = "PUBLICO") -> str:
    """
    Verifica si un hospital está adherido al convenio CAS.
    
    Args:
        hospital_id: Identificador del centro hospitalario
        convenio_tipo: Tipo de convenio (PUBLICO, PRIVADO, EMERGENCIAS)
    
    Returns:
        Estado de adhesión del hospital.
    """
    hospital = find_hospital(hospital_id)
    
    if not hospital:
        return json.dumps({
            "estado": "NO_ENCONTRADO",
            "mensaje": f"Hospital '{hospital_id}' NO encontrado en el registro de adhesiones.",
            "motivo_rehuse": "R05",
            "accion_recomendada": "Verificar el código del hospital o considerar rehúse R05."
        }, ensure_ascii=False)
    
    if not hospital["activo"]:
        return json.dumps({
            "estado": "INACTIVO",
            "nombre": hospital["nombre"],
            "mensaje": f"Hospital '{hospital['nombre']}' encontrado pero NO está activo en el convenio.",
            "motivo_rehuse": "R05",
        }, ensure_ascii=False)
    
    if hospital["convenio"].upper() != convenio_tipo.upper():
        return json.dumps({
            "estado": "CONVENIO_DIFERENTE",
            "nombre": hospital["nombre"],
            "convenio_hospital": hospital["convenio"],
            "convenio_solicitado": convenio_tipo,
            "mensaje": f"Hospital adherido al convenio {hospital['convenio']} pero se solicita {convenio_tipo}.",
            "accion_recomendada": "Verificar tipo de convenio aplicable."
        }, ensure_ascii=False)
    
    return json.dumps({
        "estado": "ADHERIDO",
        "nombre": hospital["nombre"],
        "tipo": hospital["tipo"],
        "convenio": hospital["convenio"],
        "adherido_desde": hospital["adherido_desde"],
        "provincia": hospital["provincia"],
        "mensaje": f"Hospital '{hospital['nombre']}' ADHERIDO al convenio {hospital['convenio']} desde {hospital['adherido_desde']}."
    }, ensure_ascii=False)


# ============================================================
# 6. VERIFICACIÓN DE TARIFAS Y BAREMOS
# ============================================================

def check_tariffs(servicios: str, convenio_tipo: str = "PUBLICO") -> str:
    """
    Comprueba que los importes facturados no excedan los baremos CAS.
    
    Args:
        servicios: JSON string con lista de servicios y sus importes.
                   Formato: '[{"tipo": "consulta_urgencias", "importe": 120.00}]'
        convenio_tipo: Tipo de convenio (PUBLICO o PRIVADO)
    
    Returns:
        Resultado del control de tarifas.
    """
    try:
        if isinstance(servicios, str):
            servicios_list = json.loads(servicios)
        else:
            servicios_list = servicios
    except (json.JSONDecodeError, TypeError):
        return json.dumps({
            "estado": "ERROR",
            "mensaje": "Formato de servicios no válido. Esperado: JSON array con objetos {tipo, importe}."
        }, ensure_ascii=False)
    
    if not servicios_list:
        return json.dumps({
            "estado": "SIN_SERVICIOS",
            "mensaje": "No se proporcionaron servicios para verificar."
        }, ensure_ascii=False)
    
    baremos = BAREMOS_CAS.get(convenio_tipo.upper(), BAREMOS_CAS["PUBLICO"])
    
    resultados = []
    total_facturado = 0
    total_limite = 0
    excede_baremo = False
    
    for servicio in servicios_list:
        tipo = servicio.get("tipo", "").lower()
        importe = float(servicio.get("importe", 0))
        total_facturado += importe
        
        if tipo in baremos:
            limite = baremos[tipo]["max"]
            total_limite += limite
            ok = importe <= limite
            if not ok:
                excede_baremo = True
            resultados.append({
                "servicio": baremos[tipo]["descripcion"],
                "importe_facturado": importe,
                "limite_baremo": limite,
                "dentro_de_baremo": ok,
                "exceso": round(importe - limite, 2) if not ok else 0
            })
        else:
            resultados.append({
                "servicio": tipo,
                "importe_facturado": importe,
                "limite_baremo": "NO CATALOGADO",
                "dentro_de_baremo": None,
                "nota": "Servicio no encontrado en baremos. Revisar manualmente."
            })
    
    return json.dumps({
        "estado": "EXCEDE_BAREMO" if excede_baremo else "DENTRO_DE_BAREMO",
        "total_facturado": round(total_facturado, 2),
        "desglose": resultados,
        "mensaje": "ALERTA: Algún servicio excede el baremo CAS." if excede_baremo else "Todos los importes están dentro de los baremos del convenio.",
        "motivo_rehuse": "R08" if excede_baremo else None,
        "accion_recomendada": "Rehusar parcialmente (901) los servicios que exceden baremo." if excede_baremo else "Proceder con aceptación."
    }, ensure_ascii=False)


# ============================================================
# 7. LECTURA DE DOCUMENTOS ADJUNTOS
# ============================================================

def read_attached_document(filename: str) -> str:
    """
    Lee y extrae información de un documento adjunto de la carpeta de pruebas CAS.
    Soporta PDFs e imágenes JPEG/JPG.
    
    Args:
        filename: Nombre del archivo a leer (debe estar en amv-documentacion-cas-prueba/)
    
    Returns:
        Texto extraído del documento o descripción del contenido.
    """
    filepath = TEST_CASES_DIR / filename
    
    if not filepath.exists():
        # Intentar buscar con variaciones de extensión
        for ext in ['.pdf', '.PDF', '.jpeg', '.JPEG', '.jpg', '.JPG']:
            alt = TEST_CASES_DIR / (filename.split('.')[0] + ext)
            if alt.exists():
                filepath = alt
                break
    
    if not filepath.exists():
        return json.dumps({
            "estado": "NO_ENCONTRADO",
            "mensaje": f"Archivo '{filename}' no encontrado en la carpeta de documentación CAS.",
            "archivos_disponibles": [f.name for f in TEST_CASES_DIR.iterdir()][:20] if TEST_CASES_DIR.exists() else []
        }, ensure_ascii=False)
    
    ext = filepath.suffix.lower()
    
    if ext == '.pdf':
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(filepath))
            texts = []
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    texts.append(f"--- Página {i+1} ---\n{text.strip()}")
            
            content = "\n\n".join(texts) if texts else "PDF sin texto extraíble (posiblemente escaneado)."
            
            return json.dumps({
                "estado": "LEIDO",
                "archivo": filename,
                "tipo": "PDF",
                "paginas": len(reader.pages),
                "contenido": content[:10000],  # Limitar para no exceder contexto
                "mensaje": f"Documento PDF leído ({len(reader.pages)} páginas)."
            }, ensure_ascii=False)
        except Exception as e:
            return json.dumps({
                "estado": "ERROR_LECTURA",
                "archivo": filename,
                "mensaje": f"Error leyendo PDF: {str(e)}"
            }, ensure_ascii=False)
    
    elif ext in ('.jpeg', '.jpg', '.png'):
        return json.dumps({
            "estado": "IMAGEN",
            "archivo": filename,
            "tipo": "IMAGEN",
            "tamaño_kb": round(filepath.stat().st_size / 1024, 1),
            "mensaje": "Archivo de imagen detectado. Requiere análisis visual (OCR) para extraer texto. Descripción del contenido probable basada en el contexto del expediente.",
            "nota": "Para leer el contenido de imágenes, se recomienda usar las capacidades multimodales del modelo."
        }, ensure_ascii=False)
    
    return json.dumps({
        "estado": "TIPO_NO_SOPORTADO",
        "archivo": filename,
        "mensaje": f"Tipo de archivo '{ext}' no soportado directamente."
    }, ensure_ascii=False)


# ============================================================
# 8. VERIFICACIÓN DE COHERENCIA LESIÓN-ACCIDENTE
# ============================================================

def verify_injury_consistency(tipo_lesion: str, tipo_accidente: str, posicion_vehiculo: str = "") -> str:
    """
    Cruza el tipo de lesión declarada con la dinámica del accidente para
    detectar posibles inconsistencias o fraude.
    
    Args:
        tipo_lesion: Tipo de lesión declarada (ej: "Cervicalgia", "Contusión múltiple")
        tipo_accidente: Descripción del tipo de accidente (ej: "Alcance trasero")
        posicion_vehiculo: Posición del lesionado en el vehículo (ej: "Conductor", "Acompañante")
    
    Returns:
        Resultado del análisis de coherencia.
    """
    # Mapeo de lesiones coherentes con tipos de accidente
    coherencia_map = {
        "alcance trasero": ["cervicalgia", "latigazo cervical", "contractura cervical", 
                            "contusión", "cervical", "dorsal", "lumbar"],
        "colisión lateral": ["contusión", "fractura costal", "traumatismo torácico",
                             "contusión múltiple", "hematoma", "cervical"],
        "colisión frontal": ["cervicalgia", "traumatismo craneal", "contusión múltiple",
                             "fractura", "latigazo cervical", "cervical"],
        "atropello": ["fractura", "contusión múltiple", "traumatismo", "herida",
                       "politraumatismo"],
        "vuelco": ["politraumatismo", "fractura", "contusión múltiple", "traumatismo"],
    }
    
    tipo_acc_lower = tipo_accidente.lower()
    lesion_lower = tipo_lesion.lower()
    
    # Buscar la categoría de accidente más parecida
    coherente = False
    categoria_encontrada = None
    
    for cat, lesiones_esperadas in coherencia_map.items():
        if cat in tipo_acc_lower:
            categoria_encontrada = cat
            for lesion_esperada in lesiones_esperadas:
                if lesion_esperada in lesion_lower:
                    coherente = True
                    break
            break
    
    if coherente:
        return json.dumps({
            "estado": "COHERENTE",
            "lesion": tipo_lesion,
            "accidente": tipo_accidente,
            "posicion": posicion_vehiculo,
            "mensaje": f"Lesión '{tipo_lesion}' es COHERENTE con un accidente tipo '{tipo_accidente}'.",
            "nivel_confianza": "ALTO"
        }, ensure_ascii=False)
    elif categoria_encontrada:
        return json.dumps({
            "estado": "REVISAR",
            "lesion": tipo_lesion,
            "accidente": tipo_accidente,
            "posicion": posicion_vehiculo,
            "mensaje": f"ALERTA: Lesión '{tipo_lesion}' es POCO HABITUAL para accidente tipo '{tipo_accidente}'. Las lesiones típicas para este tipo de accidente son: {coherencia_map[categoria_encontrada]}",
            "motivo_rehuse": "R06",
            "nivel_confianza": "BAJO",
            "accion_recomendada": "Solicitar documentación adicional (301) para justificar la lesión."
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "estado": "INDETERMINADO",
            "lesion": tipo_lesion,
            "accidente": tipo_accidente,
            "mensaje": f"No se puede determinar la coherencia automáticamente para tipo de accidente '{tipo_accidente}'. Requiere revisión manual.",
            "accion_recomendada": "Revisión manual por el tramitador."
        }, ensure_ascii=False)


# ============================================================
# 9. BÚSQUEDA EN HISTORIAL DEL EXPEDIENTE
# ============================================================

def search_case_history(expediente_id: str) -> str:
    """
    Busca el historial completo de un expediente CAS, incluyendo
    todos los códigos intercambiados, documentos y notas.
    
    Args:
        expediente_id: Número de expediente CAS
    
    Returns:
        Historial completo del expediente.
    """
    expediente = find_expediente(expediente_id)
    
    if not expediente:
        return json.dumps({
            "estado": "NO_ENCONTRADO",
            "mensaje": f"Expediente '{expediente_id}' no encontrado en el sistema.",
            "expedientes_disponibles": list(EXPEDIENTES_CAS.keys())
        }, ensure_ascii=False)
    
    # Obtener datos del siniestro asociado
    siniestro = find_siniestro(expediente["siniestro"]) or {}
    hospital = find_hospital(expediente["hospital"]) or {}
    
    return json.dumps({
        "estado": "ENCONTRADO",
        "expediente_id": expediente_id,
        "siniestro": expediente["siniestro"],
        "hospital": hospital.get("nombre", expediente["hospital"]),
        "convenio": expediente["convenio"],
        "estado_cas": expediente["estado_cas"],
        "ultimo_codigo": expediente["ultimo_codigo"],
        "historial_codigos": expediente["historial_codigos"],
        "documentos": expediente["documentos"],
        "fecha_apertura": expediente["fecha_apertura"],
        "importe_reclamado": expediente["importe_reclamado"],
        "importe_aceptado": expediente["importe_aceptado"],
        "datos_siniestro": {
            "fecha": siniestro.get("fecha_ocurrencia"),
            "tipo": siniestro.get("tipo"),
            "lugar": siniestro.get("lugar"),
            "lesionados": len(siniestro.get("lesionados", [])),
        },
        "mensaje": f"Expediente encontrado. Estado: {expediente['estado_cas']}. Último código: {expediente['ultimo_codigo']}."
    }, ensure_ascii=False)


# ============================================================
# 10. VALIDACIÓN DE FECHAS CAS
# ============================================================

def validate_cas_dates(fecha_ocurrencia: str, fecha_asistencia: str = "", 
                       fecha_parte: str = "") -> str:
    """
    Valida la coherencia temporal de las fechas en un expediente CAS.
    
    Args:
        fecha_ocurrencia: Fecha del accidente (YYYY-MM-DD)
        fecha_asistencia: Fecha de la asistencia hospitalaria (YYYY-MM-DD)
        fecha_parte: Fecha de envío del parte CAS (YYYY-MM-DD)
    
    Returns:
        Resultado de validación temporal.
    """
    alertas = []
    
    try:
        f_ocurrencia = datetime.strptime(fecha_ocurrencia, "%Y-%m-%d")
    except ValueError:
        return json.dumps({
            "estado": "ERROR",
            "mensaje": f"Formato de fecha de ocurrencia inválido: '{fecha_ocurrencia}'. Usar YYYY-MM-DD."
        }, ensure_ascii=False)
    
    hoy = datetime.now()
    
    # Verificar que la ocurrencia no es futura
    if f_ocurrencia > hoy:
        alertas.append("ALERTA: Fecha de ocurrencia es FUTURA.")
    
    # Verificar que no es demasiado antigua (más de 1 año)
    if (hoy - f_ocurrencia).days > 365:
        alertas.append(f"ALERTA: Siniestro de hace {(hoy - f_ocurrencia).days} días. Posible prescripción. Motivo rehúse R12.")
    
    # Verificar fecha de asistencia
    if fecha_asistencia:
        try:
            f_asistencia = datetime.strptime(fecha_asistencia, "%Y-%m-%d")
            if f_asistencia < f_ocurrencia:
                alertas.append("ALERTA: Fecha de asistencia ANTERIOR a la fecha de ocurrencia. Posible error o fraude.")
            elif (f_asistencia - f_ocurrencia).days > 30:
                alertas.append(f"ALERTA: {(f_asistencia - f_ocurrencia).days} días entre ocurrencia y asistencia. Verificar causalidad.")
        except ValueError:
            alertas.append(f"Formato de fecha de asistencia inválido: '{fecha_asistencia}'.")
    
    # Verificar fecha de parte
    if fecha_parte:
        try:
            f_parte = datetime.strptime(fecha_parte, "%Y-%m-%d")
            if f_parte < f_ocurrencia:
                alertas.append("ALERTA: Fecha de parte ANTERIOR a la fecha de ocurrencia.")
            elif (f_parte - f_ocurrencia).days > 90:
                alertas.append(f"ALERTA: Parte enviado {(f_parte - f_ocurrencia).days} días después del accidente. Plazo posiblemente excedido.")
        except ValueError:
            alertas.append(f"Formato de fecha de parte inválido: '{fecha_parte}'.")
    
    # Verificar que está dentro del período de convenio vigente
    convenio_inicio = datetime(2024, 1, 1)
    convenio_fin = datetime(2026, 12, 31)
    
    dentro_convenio = convenio_inicio <= f_ocurrencia <= convenio_fin
    if not dentro_convenio:
        alertas.append(f"ALERTA: Fecha de ocurrencia FUERA del período de convenio vigente ({convenio_inicio.date()} a {convenio_fin.date()}). Motivo rehúse R04.")
    
    return json.dumps({
        "estado": "ALERTAS" if alertas else "OK",
        "fecha_ocurrencia": fecha_ocurrencia,
        "fecha_asistencia": fecha_asistencia or "No proporcionada",
        "fecha_parte": fecha_parte or "No proporcionada",
        "dentro_convenio": dentro_convenio,
        "alertas": alertas,
        "mensaje": " | ".join(alertas) if alertas else "Todas las fechas son coherentes y están dentro del período de convenio."
    }, ensure_ascii=False)


# ============================================================
# 11. GENERACIÓN DE RESPUESTA CAS
# ============================================================

def generate_cas_response_code(expediente_id: str, codigo_respuesta: str, 
                                motivo: str = "", importe: float = 0.0) -> str:
    """
    Genera la estructura de respuesta CAS con el código apropiado.
    
    Args:
        expediente_id: Número de expediente
        codigo_respuesta: Código CAS de respuesta (200, 300, 301, 400, 600, 900, etc.)
        motivo: Motivo de la acción (especialmente para rehúse)
        importe: Importe (para aceptaciones de factura)
    
    Returns:
        Estructura de respuesta CAS formateada.
    """
    code_info = get_code_info(codigo_respuesta)
    
    if "error" in code_info:
        return json.dumps({
            "estado": "ERROR",
            "mensaje": code_info["error"]
        }, ensure_ascii=False)
    
    # Verificar transición si hay expediente
    if expediente_id:
        expediente = find_expediente(expediente_id)
        if expediente:
            transition = validate_transition(expediente["ultimo_codigo"], codigo_respuesta)
            if not transition["valid"]:
                return json.dumps({
                    "estado": "TRANSICION_INVALIDA",
                    "mensaje": transition["message"],
                    "codigos_permitidos": transition["allowed_codes"]
                }, ensure_ascii=False)
    
    response = {
        "estado": "GENERADO",
        "expediente": expediente_id,
        "codigo": codigo_respuesta,
        "nombre": code_info.get("nombre"),
        "tipo": code_info.get("tipo"),
        "emisor": "ASEGURADORA",
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "motivo": motivo,
        "contenido": {
            "codigo_respuesta": codigo_respuesta,
            "expediente_referencia": expediente_id,
            "texto_motivo": motivo or f"Respuesta estándar código {codigo_respuesta}",
        }
    }
    
    if importe > 0:
        response["contenido"]["importe"] = importe
    
    if codigo_respuesta in ["900", "901", "828"]:
        # Buscar motivo de rehúse estándar
        motivo_code = motivo if motivo in MOTIVOS_REHUSE else None
        response["contenido"]["motivo_rehuse_estandar"] = MOTIVOS_REHUSE.get(motivo, motivo)
    
    response["mensaje"] = f"Respuesta CAS generada: {codigo_respuesta} - {code_info.get('nombre')}."
    response["nota_expediente"] = f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Berta (IA): Emitida respuesta {codigo_respuesta} ({code_info.get('nombre')}). {motivo}"
    
    return json.dumps(response, ensure_ascii=False)


# ============================================================
# 12. ANÁLISIS DE CASO CAS DESDE SIAX (Botón 1)
# ============================================================

def analizar_caso_siax(id_cas: int) -> str:
    """
    Consulta SIAX para obtener todas las secuencias y mensajes de un caso CAS,
    y determina cuáles requieren respuesta por parte de la aseguradora.

    Este es el "Botón 1": analizar todas las conversaciones del caso.

    Args:
        id_cas: ID de la reclamación CAS en SIAX (lo envía SIAX en sus llamadas).

    Returns:
        Análisis completo del caso con las secuencias, mensajes y recomendaciones
        sobre cuáles pueden/deben ser respondidos.
    """
    try:
        from .siax_client import obtener_cas
    except ImportError:
        from siax_client import obtener_cas

    result = obtener_cas(id_cas)

    if not result.get("ok"):
        return json.dumps({
            "estado": "ERROR_SIAX",
            "mensaje": result.get("error", "Error desconocido al consultar SIAX"),
            "id_cas": id_cas,
        }, ensure_ascii=False)

    # Construir resumen de análisis
    resumen_secuencias = []

    for sec in result.get("secuencias", []):
        referencia = sec["referencia_cas"]
        mensajes_detalle = []

        for msg in sec.get("mensajes", []):
            info_codigo = get_code_info(msg["codigo"])
            nombre_codigo = info_codigo.get("nombre", f"Código {msg['codigo']}")

            detalle = {
                "id": msg["id"],
                "codigo": msg["codigo"],
                "nombre": nombre_codigo,
                "emisor": msg["emisor"],
                "estado": msg["estado"],
                "convenio": msg["convenio_normas"],
                "fecha_caducidad": msg["fecha_caducidad"],
                "caducado": msg["caducado"],
                "mensaje_referido": msg["mensaje_referido"],
            }

            if msg["puede_responder"]:
                detalle["puede_responder"] = True
                detalle["codigos_respuesta_validos"] = msg["codigos_respuesta_validos"]
                # Añadir nombre de cada código de respuesta
                detalle["opciones_respuesta"] = []
                for cod in msg["codigos_respuesta_validos"]:
                    cod_info = get_code_info(cod)
                    detalle["opciones_respuesta"].append({
                        "codigo": cod,
                        "nombre": cod_info.get("nombre", f"Código {cod}"),
                        "tipo": cod_info.get("tipo", "DESCONOCIDO"),
                    })
            else:
                detalle["puede_responder"] = False

            mensajes_detalle.append(detalle)

        resumen_sec = {
            "referencia_cas": referencia,
            "total_mensajes": sec["total_mensajes"],
            "ultimo_codigo": sec["ultimo_codigo"],
            "necesita_accion": sec["necesita_accion"],
            "mensajes": mensajes_detalle,
        }

        if sec["necesita_accion"]:
            resumen_sec["accion_requerida"] = (
                f"La secuencia {referencia} requiere respuesta. "
                f"Último mensaje: código {sec['ultimo_codigo']}. "
                f"Opciones de respuesta: {sec['codigos_respuesta_disponibles']}"
            )

        resumen_secuencias.append(resumen_sec)

    analisis = {
        "estado": "OK",
        "id_cas": id_cas,
        "environment": result.get("environment", "unknown"),
        "total_secuencias": result["total_secuencias"],
        "total_mensajes": result["total_mensajes"],
        "secuencias_que_requieren_accion": result["secuencias_respondibles"],
        "secuencias": resumen_secuencias,
        "instrucciones": (
            "Revisa cada secuencia. Las que tienen 'necesita_accion: true' requieren "
            "respuesta de la aseguradora. Analiza el contexto de los mensajes previos, "
            "el convenio aplicable y las fechas de caducidad para recomendar la mejor acción."
        ),
    }

    return json.dumps(analisis, ensure_ascii=False, default=str)


# ============================================================
# 13. ANÁLISIS DE MENSAJE ESPECÍFICO CAS DESDE SIAX (Botón 2)
# ============================================================

def analizar_mensaje_siax(id_cas: int, id_mensaje: int) -> str:
    """
    Consulta SIAX y analiza un mensaje específico dentro de un caso CAS,
    recomendando con qué código de respuesta responder.

    Este es el "Botón 2": analizar un mensaje concreto y recomendar respuesta.

    Args:
        id_cas: ID de la reclamación CAS en SIAX.
        id_mensaje: ID del mensaje específico a analizar.

    Returns:
        Análisis detallado del mensaje con recomendación de código de respuesta,
        contexto de la secuencia y justificación normativa.
    """
    try:
        from .siax_client import obtener_cas
    except ImportError:
        from siax_client import obtener_cas

    result = obtener_cas(id_cas)

    if not result.get("ok"):
        return json.dumps({
            "estado": "ERROR_SIAX",
            "mensaje": result.get("error", "Error desconocido al consultar SIAX"),
            "id_cas": id_cas,
            "id_mensaje": id_mensaje,
        }, ensure_ascii=False)

    # Buscar el mensaje específico y su secuencia
    mensaje_encontrado = None
    secuencia_contexto = None

    for sec in result.get("secuencias", []):
        for msg in sec.get("mensajes", []):
            if msg["id"] == id_mensaje:
                mensaje_encontrado = msg
                secuencia_contexto = sec
                break
        if mensaje_encontrado:
            break

    if not mensaje_encontrado:
        return json.dumps({
            "estado": "MENSAJE_NO_ENCONTRADO",
            "mensaje": f"No se encontró el mensaje con ID {id_mensaje} en el caso CAS {id_cas}.",
            "id_cas": id_cas,
            "id_mensaje": id_mensaje,
            "mensajes_disponibles": [
                {"id": m["id"], "codigo": m["codigo"], "secuencia": s["referencia_cas"]}
                for s in result.get("secuencias", [])
                for m in s.get("mensajes", [])
            ],
        }, ensure_ascii=False)

    # Obtener información del código
    codigo = mensaje_encontrado["codigo"]
    info_codigo = get_code_info(codigo)

    # Construir historial de la secuencia hasta este mensaje
    historial = []
    for msg in secuencia_contexto.get("mensajes", []):
        msg_info = get_code_info(msg["codigo"])
        historial.append({
            "id": msg["id"],
            "codigo": msg["codigo"],
            "nombre": msg_info.get("nombre", f"Código {msg['codigo']}"),
            "emisor": msg["emisor"],
            "estado": msg["estado"],
            "fecha_caducidad": msg["fecha_caducidad"],
            "mensaje_referido": msg["mensaje_referido"],
        })
        if msg["id"] == id_mensaje:
            break

    # Determinar opciones de respuesta
    codigos_respuesta = mensaje_encontrado.get("codigos_respuesta_validos", [])
    opciones = []
    for cod in codigos_respuesta:
        cod_info = get_code_info(cod)
        accion = get_required_action(cod) if cod in CAS_CODES else ""
        opciones.append({
            "codigo": cod,
            "nombre": cod_info.get("nombre", f"Código {cod}"),
            "tipo": cod_info.get("tipo", "DESCONOCIDO"),
            "descripcion": cod_info.get("descripcion", ""),
            "accion_asociada": accion,
        })

    # Construir el análisis del mensaje
    analisis = {
        "estado": "OK",
        "id_cas": id_cas,
        "id_mensaje": id_mensaje,
        "referencia_cas": secuencia_contexto["referencia_cas"],
        "mensaje": {
            "id": mensaje_encontrado["id"],
            "codigo": codigo,
            "nombre": info_codigo.get("nombre", f"Código {codigo}"),
            "emisor": mensaje_encontrado["emisor"],
            "estado": mensaje_encontrado["estado"],
            "convenio_normas": mensaje_encontrado["convenio_normas"],
            "fecha_caducidad": mensaje_encontrado["fecha_caducidad"],
            "caducado": mensaje_encontrado["caducado"],
            "puede_responder": mensaje_encontrado["puede_responder"],
        },
        "historial_secuencia": historial,
        "opciones_respuesta": opciones,
        "instrucciones": (
            f"Analiza el mensaje {codigo} ({info_codigo.get('nombre', '')}) "
            f"recibido en la secuencia {secuencia_contexto['referencia_cas']}. "
            f"Convenio: {mensaje_encontrado['convenio_normas']}. "
            f"Considerando el historial de la secuencia y la normativa CAS aplicable, "
            f"recomienda CON CUÁL de las opciones de respuesta ({codigos_respuesta}) "
            f"debe responder la aseguradora. Justifica tu recomendación con referencias "
            f"al convenio y la normativa de procedimiento general."
        ),
    }

    return json.dumps(analisis, ensure_ascii=False, default=str)
