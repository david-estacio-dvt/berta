# Documentación del Proyecto: Tramitación CAS con IA

Extraído de las imágenes proporcionadas (Planteamiento Tramitación CAS con IA).

## 1. Contexto: Convenio de Asistencia Sanitaria (CAS)
El proyecto busca automatizar la gestión de facturación y pago de prestaciones sanitarias por accidentes de circulación entre Entidades Aseguradoras y Centros Hospitalarios.
Existen diferentes convenios (Sanitario Público, Sanitario Privado, Emergencias).

## 2. Características del Servicio
- **Sistema Central**: Aplicación web centralizada (sistema de mensajería).
- **Comunicación**: Basada en intercambios de **códigos**.
- **Reglas**: Manual de criterios con secuencias y plazos de caducidad.
- **Datos Obligatorios**: Fecha ocurrencia, vehículos implicados, datos lesionados, posición en el vehículo, lesión producida, datos del hospital.

## 3. Flujo del Proceso (Diálogo)
1.  **Inicio**: El Centro Hospitalario inicia el diálogo enviando el "Parte de Asistencia" con un código específico.
2.  **Respuesta Aseguradora**: Debe contestar aceptando o rechazando el parte (si no cumple normativa o datos incorrectos).
3.  **Documentación**: Durante el diálogo, el hospital adjunta informes médicos acreditando la lesión y el tratamiento.
4.  **Revisión**: La entidad aseguradora revisa la documentación para ver si justifica el tratamiento.
5.  **Resolución Intermedia**: La aseguradora autoriza o rechaza facturas con códigos correspondientes.
6.  **Cierre**: El diálogo finaliza con un código de "baja", "pago" o "rehúse".

## 4. Requerimientos para el Agente de IA (Herramienta de Apoyo)
El agente debe ser capaz de:
- **Lógica de Códigos**: Disponer de toda la secuencia de códigos según los manuales de cada convenio.
- **Identificación**: Identificar convenios y hospitales adheridos.
- **Comprobaciones Iniciales**: Validar cobertura, riesgo, fecha inicio convenio CAS, siniestralidad del colegio.
- **Lectura de Documentos**: Leer la documentación intercambiada en el diálogo (PDFs, imágenes).
- **Detección de Inconsistencias**: Cruzar datos con el histórico de la aplicación (notas, lesionado, tipo de lesiones, ocurrencia).
- **Intervención**: Responder en el diálogo marcando los códigos correspondientes y las sumas de cada convenio.
- **Gestión de Documentos**: Adjuntar documentos si el diálogo lo requiere.
- **Toma de Decisiones**: Aceptar o rehusar tratamiento tras comprobar documentación vs información disponible.
- **Alertas**: Generar alertas al tramitador si hay incongruencias (lesión vs tratamiento).
- **Notas y Auditoría**: Generar notas en el histórico con la gestión realizada y el motivo.
- **Control Económico**: Realizar controles de tarifas y límites económicos según convenio.
- **Cierre de Facturación**: Aceptar abono solo si cumple normas. Cerrar tramitación cuando finalice.
