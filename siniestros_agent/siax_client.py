"""
siax_client.py - Cliente REST para el servicio web ServiciosGemini (SIAX).

Permite consultar datos de reclamaciones CAS desde SIAX a través de la API
REST de ServiciosGemini (ObtenerCas / GetTest).

URLs:
  Test:       https://desarrollo.senassur.com/ServiciosGemini.svc/rest/ObtenerCas
  Producción: https://www.senassur.com:8086/Xena/ServiciosGemini.svc/rest/ObtenerCas
"""

import os
import json
import requests
from datetime import datetime
from typing import Optional


# ─────────────────────────────────────────────
# Configuración
# ─────────────────────────────────────────────

SIAX_URLS = {
    "test": "https://desarrollo.senassur.com/ServiciosGemini.svc",
    "produccion": "https://www.senassur.com:8086/Xena/ServiciosGemini.svc",
}

DEFAULT_TIMEOUT = 30  # segundos


def _get_config() -> dict:
    """Obtiene la configuración SIAX desde variables de entorno."""
    env = os.environ.get("SIAX_ENVIRONMENT", "test").lower()
    base_url = os.environ.get("SIAX_URL") or SIAX_URLS.get(env, SIAX_URLS["test"])

    # Normalizar: quitar suffijo /rest si lo tiene (se añade en cada llamada)
    base_url = base_url.rstrip("/")
    if base_url.endswith("/rest"):
        base_url = base_url[:-5]

    return {
        "username": os.environ.get("SIAX_USERNAME", ""),
        "password": os.environ.get("SIAX_PASSWORD", ""),
        "base_url": base_url,
        "environment": env,
    }


# ─────────────────────────────────────────────
# API Calls
# ─────────────────────────────────────────────

def test_conexion() -> dict:
    """
    Llama al método GetTest() del servicio para verificar conectividad.
    No requiere autenticación.

    Returns:
        Dict con {ok: bool, mensaje: str, url: str}
    """
    config = _get_config()
    url = f"{config['base_url']}/rest/GetTest"

    try:
        resp = requests.get(url, timeout=DEFAULT_TIMEOUT, verify=True)
        resp.raise_for_status()

        return {
            "ok": True,
            "mensaje": resp.text,
            "url": url,
            "environment": config["environment"],
            "status_code": resp.status_code,
        }
    except requests.exceptions.ConnectionError as e:
        return {
            "ok": False,
            "mensaje": f"Error de conexión con SIAX: {str(e)}",
            "url": url,
            "environment": config["environment"],
        }
    except requests.exceptions.Timeout:
        return {
            "ok": False,
            "mensaje": f"Timeout al conectar con SIAX (>{DEFAULT_TIMEOUT}s)",
            "url": url,
            "environment": config["environment"],
        }
    except requests.exceptions.HTTPError as e:
        return {
            "ok": False,
            "mensaje": f"Error HTTP de SIAX: {resp.status_code} - {resp.text}",
            "url": url,
            "environment": config["environment"],
        }
    except Exception as e:
        return {
            "ok": False,
            "mensaje": f"Error inesperado: {str(e)}",
            "url": url,
            "environment": config["environment"],
        }


def obtener_cas(id_cas: int) -> dict:
    """
    Llama al método ObtenerCas del servicio ServiciosGemini.

    Obtiene las secuencias y mensajes CAS asociados a una reclamación.

    Args:
        id_cas: ID de la reclamación CAS en SIAX.

    Returns:
        Dict con las secuencias parseadas, o error si falla.
    """
    config = _get_config()

    if not config["username"] or not config["password"]:
        return {
            "ok": False,
            "error": "Credenciales SIAX no configuradas. Establecer SIAX_USERNAME y SIAX_PASSWORD en .env",
        }

    url = f"{config['base_url']}/rest/ObtenerCas"
    payload = {
        "username": config["username"],
        "password": config["password"],
        "idCas": id_cas,
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=DEFAULT_TIMEOUT,
            verify=True,
        )
        resp.raise_for_status()
        data = resp.json()

        # Parsear la respuesta
        return _parsear_respuesta_cas(data, id_cas, config["environment"])

    except requests.exceptions.ConnectionError as e:
        return {
            "ok": False,
            "error": f"Error de conexión con SIAX: {str(e)}",
            "id_cas": id_cas,
            "url": url,
        }
    except requests.exceptions.Timeout:
        return {
            "ok": False,
            "error": f"Timeout al consultar SIAX (>{DEFAULT_TIMEOUT}s)",
            "id_cas": id_cas,
            "url": url,
        }
    except requests.exceptions.HTTPError:
        return {
            "ok": False,
            "error": f"Error HTTP: {resp.status_code} - {resp.text[:500]}",
            "id_cas": id_cas,
            "url": url,
        }
    except json.JSONDecodeError:
        return {
            "ok": False,
            "error": f"Respuesta no es JSON válido: {resp.text[:500]}",
            "id_cas": id_cas,
            "url": url,
        }
    except Exception as e:
        return {
            "ok": False,
            "error": f"Error inesperado: {str(e)}",
            "id_cas": id_cas,
            "url": url,
        }


# ─────────────────────────────────────────────
# Parsing de respuesta
# ─────────────────────────────────────────────

# Códigos CAS emitidos por el HOSPITAL (CH) — la aseguradora puede/debe responder
CODIGOS_HOSPITAL = {
    # Partes iniciales
    "47", "101", "102", "170", "171", "172", "173", "174", "175", "176",
    # Facturación
    "181",
    # Traslados
    "191", "192",
    # Comunicaciones y documentación del hospital
    "301", "302", "306", "308", "309", "315",
    "363", "364", "365", "366", "369", "370", "373", "376", "377", "379", "384",
    "391", "392", "393", "395",
    # Cierre por hospital
    "500", "501", "504",
    # Facturación rectificativa
    "580", "581", "582", "583", "585", "587",
    # Documentación clínica / originales
    "801", "806", "811", "814", "821", "822", "823", "824", "825",
    "863", "864", "865", "866", "869", "877", "879", "881", "885",
    "891", "892", "893", "895",
    # Subcomisiones/alegaciones del hospital
    "652", "653", "664", "665", "670", "671",
}

# Códigos CAS emitidos por la ASEGURADORA (EA)
CODIGOS_ASEGURADORA = {
    # Aceptaciones
    "201", "202", "203", "271", "281",
    # Documentación y comunicaciones
    "303", "304", "305", "311", "314", "316", "317", "318",
    "319", "320", "321", "322", "323", "324",
    "360", "361", "362", "367", "368", "371", "372", "374", "378", "380", "381", "383", "387",
    "390", "394", "398", "399",
    # Rechazos de partes
    "401", "403", "422", "423",
    "471", "472", "473", "474", "475", "476", "477",
    # Rechazos de facturas
    "442", "443", "481", "482", "483", "484", "485", "486", "487", "488",
    # Rechazos generales
    "492", "494", "495", "496", "497", "498", "499",
    # Documentación original EA
    "841", "861", "867", "870", "874", "878", "880", "890", "894", "898", "899",
}

# Códigos CAS emitidos por el SISTEMA / Comisión / Subcomisión (CS)
CODIGOS_SISTEMA = {
    "270", "272", "275", "280", "284", "285", "287", "288",
    "310", "312", "313", "325", "326", "327", "375",
    "421", "478", "484",
    "502", "503", "570", "572", "573", "574", "575", "576", "577", "578", "579", "584", "586",
    "655", "662", "663", "666", "667", "669", "672", "673", "674", "676", "677", "678", "679",
    "682", "683", "684", "685", "687",
    "715", "716", "717",
    "896", "897",
}

# Transiciones válidas: desde código recibido del hospital → posibles respuestas de la aseguradora
TRANSICIONES_RESPUESTA = {
    # Partes de asistencia → aceptar, rechazar, solicitar aclaración
    "101": ["201", "401", "471", "472", "492", "494"],
    "171": ["271", "471", "472", "473", "474", "475", "476", "477", "492", "494", "495", "496", "497", "498", "499"],
    "172": ["271", "471", "472", "473", "474", "475", "476", "477"],
    "173": ["271", "471", "472", "473"],
    "174": ["271", "471", "472", "473"],
    "175": ["271", "471", "472", "475", "476"],
    "176": ["271", "471", "476"],
    # Facturas → aceptar, rechazar
    "181": ["281", "481", "482", "483", "485", "486", "487", "488", "368"],
    # Traslados
    "191": ["271", "471"],
    "192": ["271", "471"],
    # Comunicaciones del hospital
    "301": ["202", "311", "362"],
    "302": ["303", "304", "305"],
    "306": ["303", "304"],
    "315": ["316", "317"],
    "363": ["362"],
    "369": ["281", "481"],
    "370": ["371", "372"],
    # Documentación clínica
    "801": ["203", "403"],
    "811": ["362"],
    "823": ["319", "320"],
    "824": ["321", "322"],
    "825": ["323", "324"],
}


def _inferir_emisor(codigo: str) -> str:
    """Infiere quién emitió el mensaje basado en el código."""
    if codigo in CODIGOS_HOSPITAL:
        return "HOSPITAL"
    elif codigo in CODIGOS_ASEGURADORA:
        return "ASEGURADORA"
    elif codigo in CODIGOS_SISTEMA:
        return "SISTEMA"
    else:
        return "DESCONOCIDO"


def _parsear_fecha(fecha_str: str) -> Optional[datetime]:
    """Parsea fecha en formato dd/MM/yyyy H:mm:ss."""
    if not fecha_str:
        return None
    try:
        # Formato: "01/08/2024 0:00:00"
        return datetime.strptime(fecha_str.strip(), "%d/%m/%Y %H:%M:%S")
    except ValueError:
        try:
            return datetime.strptime(fecha_str.strip(), "%d/%m/%Y")
        except ValueError:
            return None


def _esta_caducado(fecha_caducidad_str: str) -> bool:
    """Determina si un mensaje ha caducado."""
    fecha = _parsear_fecha(fecha_caducidad_str)
    if not fecha:
        return False
    return datetime.now() > fecha


def _parsear_respuesta_cas(data: dict, id_cas: int, environment: str) -> dict:
    """
    Parsea la respuesta JSON del servicio ObtenerCas y enriquece
    cada mensaje con información de análisis.
    """
    result_key = "ObtenerCasResult"
    if result_key not in data:
        return {
            "ok": False,
            "error": f"Respuesta inesperada de SIAX. Claves: {list(data.keys())}",
            "id_cas": id_cas,
            "data_raw": data,
        }

    secuencias_raw = data[result_key].get("Secuencias", [])

    secuencias = []
    total_mensajes = 0
    mensajes_respondibles = 0

    for sec_raw in secuencias_raw:
        referencia = sec_raw.get("ReferenciaCas", "")
        mensajes_raw = sec_raw.get("MensajesCas", [])

        mensajes = []
        for msg_raw in mensajes_raw:
            codigo = str(msg_raw.get("Codigo", ""))
            estado = msg_raw.get("Estado", "")
            fecha_cad = msg_raw.get("FechaCaducidad", "")
            emisor = _inferir_emisor(codigo)
            caducado = _esta_caducado(fecha_cad)

            # Determinar si la aseguradora puede/debe responder
            # Solo si el úlimo mensaje de la secuencia es del hospital
            # y no está caducado
            codigos_respuesta = TRANSICIONES_RESPUESTA.get(codigo, [])
            puede_responder = (
                emisor == "HOSPITAL"
                and estado == "Recibido"
                and not caducado
                and len(codigos_respuesta) > 0
            )

            mensaje = {
                "id": msg_raw.get("Id"),
                "codigo": codigo,
                "convenio_normas": msg_raw.get("ConvenioNormas", ""),
                "estado": estado,
                "fecha_caducidad": fecha_cad,
                "mensaje_referido": msg_raw.get("MensajeReferido"),
                "emisor": emisor,
                "caducado": caducado,
                "puede_responder": puede_responder,
                "codigos_respuesta_validos": codigos_respuesta if puede_responder else [],
            }
            mensajes.append(mensaje)
            total_mensajes += 1

        # Determinar el último mensaje de la secuencia y si necesita acción
        ultimo_mensaje = mensajes[-1] if mensajes else None
        necesita_accion = (
            ultimo_mensaje is not None
            and ultimo_mensaje["emisor"] == "HOSPITAL"
            and ultimo_mensaje["estado"] == "Recibido"
            and not ultimo_mensaje["caducado"]
        )

        secuencia = {
            "referencia_cas": referencia,
            "mensajes": mensajes,
            "total_mensajes": len(mensajes),
            "ultimo_codigo": ultimo_mensaje["codigo"] if ultimo_mensaje else None,
            "ultimo_estado": ultimo_mensaje["estado"] if ultimo_mensaje else None,
            "necesita_accion": necesita_accion,
            "codigos_respuesta_disponibles": (
                ultimo_mensaje["codigos_respuesta_validos"] if necesita_accion else []
            ),
        }
        secuencias.append(secuencia)

        if necesita_accion:
            mensajes_respondibles += 1

    return {
        "ok": True,
        "id_cas": id_cas,
        "environment": environment,
        "total_secuencias": len(secuencias),
        "total_mensajes": total_mensajes,
        "secuencias_respondibles": mensajes_respondibles,
        "secuencias": secuencias,
    }


# ─────────────────────────────────────────────
# Standalone test
# ─────────────────────────────────────────────

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    print("=== Test de conexión SIAX ===")
    result = test_conexion()
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result.get("ok"):
        print("\n=== Obtener CAS (idCas=15) ===")
        cas = obtener_cas(15)
        print(json.dumps(cas, indent=2, ensure_ascii=False, default=str))
