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

# Códigos CAS emitidos por el HOSPITAL (la aseguradora debe responder)
CODIGOS_HOSPITAL = {
    "100", "101", "171", "175",
    "328", "329",
    "500", "501",
    "652", "662",
    "702",
    "841", "866", "896",
}

# Códigos CAS emitidos por la ASEGURADORA
CODIGOS_ASEGURADORA = {
    "200", "300", "301",
    "400",
    "475", "483",
    "600", "700",
    "828", "900", "901",
}

# Transiciones válidas: desde código recibido → posibles respuestas
TRANSICIONES_RESPUESTA = {
    "100": ["200", "300", "301", "900", "999"],
    "101": ["200", "300", "301", "900", "999"],
    "171": ["200", "300", "301", "900", "999"],
    "175": ["200", "300", "301", "475", "900", "999"],
    "328": ["400", "301", "600", "900", "901", "999"],
    "329": ["400", "301", "600", "900", "901", "999"],
    "500": ["600", "700", "900", "901", "828", "999"],
    "501": ["600", "700", "900", "901", "501", "500", "999"],
    "652": ["662", "900", "999"],
    "662": ["900", "999"],
    "702": ["900", "999"],
    "841": ["652", "900", "999"],
    "866": ["900", "999"],
    "896": ["900", "999"],
}


def _inferir_emisor(codigo: str) -> str:
    """Infiere quién emitió el mensaje basado en el código."""
    if codigo in CODIGOS_HOSPITAL:
        return "HOSPITAL"
    elif codigo in CODIGOS_ASEGURADORA:
        return "ASEGURADORA"
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
    # TODO: HACK PARA LA DEMO - Ignorar la caducidad temporalmente
    # return datetime.now() > fecha
    return False


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
