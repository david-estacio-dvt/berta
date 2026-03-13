"""
demo_cases.py - Casos de demo realistas para la presentación.

Cada caso simula un mensaje CAS real tal como llegaría en producción
desde el sistema centralizado de los hospitales.

USO: Copiar y pegar cualquier caso en el chat de ADK web (adk web → http://localhost:8000)
"""

# ============================================================
# CASO 1: PARTE INICIAL ESTÁNDAR - Aceptación directa
# (Todos los datos correctos, hospital adherido, póliza vigente)
# ============================================================

CASO_1_ACEPTACION = """
NUEVO MENSAJE CAS RECIBIDO - Expediente: 202600086262

📩 Mensaje entrante del sistema CAS:
- Código CAS: 100 (Parte de Asistencia Inicial)
- Hospital: HOSP_001 (Hospital General Universitario)
- Convenio: Sanitario Público

Datos del Parte:
- Fecha de ocurrencia del siniestro: 2025-11-15
- Matrícula vehículo asegurado: 1234ABC
- Segunda matrícula implicada: XXXX999
- Lesionado: Juan García López
- DNI lesionado: 12345678A
- Posición en vehículo: Conductor
- Tipo de accidente: Colisión trasera en vía urbana
- Lesión declarada: Cervicalgia postraumática
- Siniestro referencia: SIN-2024-001

Documentación adjunta:
- 202600086262-107636405-001.PDF.pdf (Informe de urgencias)
- 202600086262-107636417-001.PDF.pdf (Parte de lesiones)
- 202600086262-107636429-001.PDF.pdf (Justificante de asistencia)

Por favor, analiza este parte y dame tu decisión con justificación completa.
"""


# ============================================================
# CASO 2: REHÚSE - Póliza expirada
# (Hospital adherido pero la póliza no estaba vigente en la fecha del accidente)
# ============================================================

CASO_2_REHUSE_POLIZA = """
NUEVO MENSAJE CAS RECIBIDO - Expediente: 202600091472

📩 Mensaje entrante del sistema CAS:
- Código CAS: 100 (Parte de Asistencia Inicial)
- Hospital: HOSP_002 (Hospital San Rafael)
- Convenio: Sanitario Público

Datos del Parte:
- Fecha de ocurrencia del siniestro: 2024-06-20
- Matrícula vehículo: 3456JKL
- Lesionado: Ana López Díaz
- DNI lesionado: 55667788D
- Posición en vehículo: Conductora
- Tipo de accidente: Colisión lateral en cruce
- Lesión declarada: Contusión en rodilla derecha

Documentación adjunta:
- 202600091472-107699134-001.pdf.pdf (Informe médico)
- 202600091472-107699139-001.pdf.pdf (Radiografía)
- 202600091472-107780594-001.pdf.pdf (Parte de asistencia hospitalaria)

Analiza este caso y dime si acepto o rehúso con la justificación normativa correspondiente.
"""


# ============================================================
# CASO 3: SOLICITUD DE DOCUMENTACIÓN - Lesión sospechosa
# (Póliza y hospital OK, pero la lesión no es coherente con el accidente)
# ============================================================

CASO_3_DOCUMENTACION = """
NUEVO MENSAJE CAS RECIBIDO - Expediente: 202500692682

📩 Mensaje entrante del sistema CAS:
- Código CAS: 100 (Parte de Asistencia Inicial)
- Hospital: HOSP_004 (Hospital Virgen del Rocío)
- Convenio: Sanitario Público

Datos del Parte:
- Fecha de ocurrencia del siniestro: 2025-12-05
- Matrícula vehículo: 5678DEF
- Lesionado: María Fernández Ruiz
- DNI lesionado: 87654321B
- Posición en vehículo: Conductora
- Tipo de accidente: Alcance trasero a baja velocidad en parking
- Lesión declarada: Fractura de fémur y traumatismo craneoencefálico

Los documentos adjuntos incluyen:
- 202500692682-104747458-001.pdf.pdf (Informe clínico inicial)
- 202500692682-104747497-001.pdf.pdf (TAC craneal)
- 202500692682-105413311-001.pdf.pdf (Informe traumatología)
- 202500692682-105925177-001.pdf.pdf (Seguimiento)

⚠️ NOTA: La lesión declarada (fractura de fémur + TCE) parece muy grave para un alcance trasero a baja velocidad en parking. Por favor, verifica la coherencia.
"""


# ============================================================
# CASO 4: CONTINUACIÓN DE EXPEDIENTE - Recepción de documentación
# (El hospital envía documentación clínica tras nuestra solicitud)
# ============================================================

CASO_4_CONTINUACION = """
NUEVO MENSAJE CAS RECIBIDO - Expediente existente: 202500399716

📩 Mensaje entrante del sistema CAS:
- Código CAS: 328 (Envío de Documentación Clínica)
- Hospital: HOSP_001 (Hospital General Universitario)
- Expediente en curso - último código: 301 (Solicitud de Documentación)

El hospital responde a nuestra solicitud de documentación adicional con los siguientes archivos:
- 202500399716-102175214-001.PDF.pdf (Informe médico ampliado)
- 202500399716-102569328-001.pdf.pdf (Evolución clínica)
- 202500399716-102772724-001.PDF.pdf (Alta médica)

Por favor, confirma recepción (código 400), revisa la documentación y dime si con esta información podemos proceder a aceptar o necesitamos algo más.
"""


# ============================================================
# CASO 5: FACTURACIÓN - Control de tarifas
# (Hospital envía factura, hay que verificar baremos)
# ============================================================

CASO_5_FACTURACION = """
NUEVO MENSAJE CAS RECIBIDO - Expediente existente: 202400926113

📩 Mensaje entrante del sistema CAS:
- Código CAS: 500 (Factura / Cierre de Asistencia)
- Hospital: HOSP_002 (Hospital San Rafael)
- Expediente en curso - historial: 100 → 200 → 328 → 400

Factura presentada:
- Consulta de urgencias: 140.00€
- Radiografía cervical: 45.00€
- TAC cervical: 240.00€
- Collarín cervical: 22.00€
- 10 sesiones rehabilitación: 350.00€ (35€/sesión)
- TOTAL: 797.00€

Convenio: Sanitario Público

Documentación adjunta:
- 202400926113-99147021-001.pdf.pdf (Factura detallada con desglose)

Verifica que los importes están dentro de los baremos del convenio público y dame tu análisis.
"""


# ============================================================
# CASO 6: HOSPITAL NO ADHERIDO
# ============================================================

CASO_6_HOSPITAL_NO_ADHERIDO = """
NUEVO MENSAJE CAS RECIBIDO - Expediente: 202600099999

📩 Mensaje entrante del sistema CAS:
- Código CAS: 171 (Parte de Asistencia Inicial)
- Hospital: HOSP_DESCONOCIDO (Clínica Privada Los Olivos)
- Convenio: Sanitario Privado

Datos del Parte:
- Fecha de ocurrencia: 2026-01-15
- Matrícula: 9012GHI
- Lesionado: Pedro Martínez Sánchez
- DNI: 11223344C
- Posición: Conductor
- Tipo de accidente: Alcance trasero en autopista
- Lesión: Latigazo cervical

¿Acepto este parte o hay algún problema?
"""



# ============================================================
# CASO 7: SIAX REAL — Análisis de caso completo (Botón 1)
# (Datos reales desde el sistema SIAX / ServiciosGemini)
# ============================================================

CASO_7_SIAX_COMPLETO = """
Analiza el caso CAS con id 200233253 desde SIAX.

Quiero que consultes el sistema SIAX, obtengas todas las secuencias y mensajes de este caso real, y me digas:
1. Cuántas secuencias tiene y cuántos mensajes
2. Cuáles de esos mensajes necesitan respuesta por nuestra parte
3. Qué códigos de respuesta son válidos para cada uno
4. Si hay algún mensaje próximo a caducar
5. Un resumen de las acciones pendientes
"""


# ============================================================
# CASO 8: SIAX REAL — Recomendar respuesta a mensaje (Botón 2)
# (Pedir a Berta que recomiende un código de respuesta para un
#  mensaje específico del caso real)
# ============================================================

CASO_8_SIAX_MENSAJE = """
Del caso CAS 200233253 en SIAX, analiza el último mensaje recibido que necesite respuesta y recomiéndame qué código de respuesta CAS enviar, con justificación normativa completa.
"""


# ============================================================
# CASO 9: SIAX REAL — Flujo completo de análisis + respuesta
# (Combina Botón 1 + Botón 2 en un solo flujo conversacional)
# ============================================================

CASO_9_SIAX_FLUJO = """
Necesito que hagas un análisis completo del caso CAS 200233253 desde SIAX:

1. Primero, analiza el caso completo y dime todas las conversaciones activas
2. Para cada mensaje que necesite respuesta, recomiéndame el código CAS más apropiado
3. Prioriza por urgencia (fecha de caducidad más próxima primero)
4. Dame un resumen ejecutivo al final con todas las acciones que debo tomar
"""


if __name__ == "__main__":
    print("=" * 70)
    print("CASOS DE DEMO - AGENTE CAS 'BERTA'")
    print("=" * 70)
    print()
    print("Copiar y pegar cualquiera de estos casos en el chat de ADK web")
    print("para ver cómo Berta analiza y responde.")
    print()
    print("─" * 70)
    print("📦 CASOS CON DATOS SIMULADOS (no requieren conexión)")
    print("─" * 70)
    
    cases_mock = [
        ("CASO 1", "Aceptación directa (todo OK)", CASO_1_ACEPTACION),
        ("CASO 2", "Rehúse por póliza expirada", CASO_2_REHUSE_POLIZA),
        ("CASO 3", "Solicitar documentación (lesión sospechosa)", CASO_3_DOCUMENTACION),
        ("CASO 4", "Continuación expediente (recepción docs)", CASO_4_CONTINUACION),
        ("CASO 5", "Facturación (control de tarifas)", CASO_5_FACTURACION),
        ("CASO 6", "Hospital no adherido", CASO_6_HOSPITAL_NO_ADHERIDO),
    ]
    
    for name, desc, case_text in cases_mock:
        print(f"📋 {name}: {desc}")
        print(f"   Primeras líneas: {case_text.strip().split(chr(10))[0]}")
        print()
    
    print("─" * 70)
    print("🔗 CASOS CON DATOS REALES SIAX (requieren conexión a ServiciosGemini)")
    print("─" * 70)
    
    cases_siax = [
        ("CASO 7", "SIAX — Análisis caso completo (Botón 1)", CASO_7_SIAX_COMPLETO),
        ("CASO 8", "SIAX — Recomendar respuesta (Botón 2)", CASO_8_SIAX_MENSAJE),
        ("CASO 9", "SIAX — Flujo completo análisis + respuesta", CASO_9_SIAX_FLUJO),
    ]
    
    for name, desc, case_text in cases_siax:
        print(f"🔗 {name}: {desc}")
        print(f"   Primeras líneas: {case_text.strip().split(chr(10))[0]}")
        print()
    
    print("=" * 70)
    print()
    print("💡 Para los casos SIAX, asegúrate de tener configurado el .env con")
    print("   SIAX_USERNAME, SIAX_PASSWORD y SIAX_URL")
    print()
