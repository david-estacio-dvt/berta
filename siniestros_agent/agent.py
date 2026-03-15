"""
Agente CAS "Berta" - Tramitadora Experta en Siniestros AMV.

Agente ADK nativo para gestión automatizada de expedientes del
Convenio de Asistencia Sanitaria (CAS).

Ejecución: adk web
"""

import os
import sys
import warnings

# Añadir el padre (scratch) al path para que "siniestros_agent" se resuelva como paquete
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Suprimir warnings de protobuf/grpc si los hay
warnings.filterwarnings("ignore", category=UserWarning)

from google.adk.agents import Agent

from siniestros_agent.tools import (
    verify_injured_person,
    verify_insurance_policy,
    verify_accident,
    check_cas_code_sequence,
    check_hospital_adhesion,
    check_tariffs,
    read_attached_document,
    verify_injury_consistency,
    search_case_history,
    validate_cas_dates,
    generate_cas_response_code,
    analizar_caso_siax,
    analizar_mensaje_siax,
)

from siniestros_agent.prompts import BERTA_SYSTEM_INSTRUCTION
from siniestros_agent.knowledge_loader import load_all_documents

# --- Configuración ---
MODEL_NAME = os.environ.get("CAS_MODEL", "gemini-2.5-pro")
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "pmo-piloto-gemini-enterprise")
GOOGLE_CLOUD_LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west1")

# --- Cargar Base de Conocimiento ---
print(f"🧠 Cargando base de conocimiento normativa CAS...")
KNOWLEDGE_BASE = load_all_documents()

# --- Construir instrucciones con la base de conocimiento ---
# Limitar la KB para no exceder el contexto del modelo
MAX_KB_CHARS = 200000  # ~50K tokens aprox
kb_text = KNOWLEDGE_BASE[:MAX_KB_CHARS]
if len(KNOWLEDGE_BASE) > MAX_KB_CHARS:
    kb_text += "\n\n[... Base de conocimiento truncada por límite de contexto ...]"

instructions = BERTA_SYSTEM_INSTRUCTION.format(knowledge_base=kb_text)

print(f"📋 Instrucciones: {len(instructions)} caracteres")
print(f"🤖 Modelo: {MODEL_NAME}")

# --- Definir el Agente ADK ---
root_agent = Agent(
    name="berta_cas_agent",
    model=MODEL_NAME,
    description="Berta - Tramitadora Experta CAS. Gestiona expedientes de siniestros sanitarios del Convenio de Asistencia Sanitaria (CAS) entre hospitales y entidades aseguradoras.",
    instruction=instructions,
    tools=[
        verify_injured_person,
        verify_insurance_policy,
        verify_accident,
        check_cas_code_sequence,
        check_hospital_adhesion,
        check_tariffs,
        read_attached_document,
        verify_injury_consistency,
        search_case_history,
        validate_cas_dates,
        generate_cas_response_code,
        analizar_caso_siax,
        analizar_mensaje_siax,
    ],
)

print(f"✅ Agente 'Berta CAS' inicializado correctamente.")
print(f"   Herramientas disponibles: {len(root_agent.tools)}")
print(f"   Ejecutar: adk web")
