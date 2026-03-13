"""
queue_manager.py - Gestión de la cola de validación humana.

Almacena en SQLite los análisis de Berta pendientes de revisión.
En producción se puede sustituir por PostgreSQL cambiando la URL de conexión.
"""

import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from schemas import BertaResponse, ValidacionHumana, ItemCola, EstadoValidacion

DB_PATH = Path(__file__).parent / "berta_cola.sqlite"


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crea las tablas necesarias si no existen."""
    conn = _get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cola_validacion (
            id_analisis         TEXT PRIMARY KEY,
            expediente_id       TEXT NOT NULL,
            codigo_cas          TEXT NOT NULL,
            decision_berta      TEXT NOT NULL,
            confianza           TEXT NOT NULL,
            estado_cola         TEXT NOT NULL,
            estado_validacion   TEXT NOT NULL DEFAULT 'PENDIENTE',
            timestamp_analisis  TEXT NOT NULL,
            timestamp_validacion TEXT,
            tramitador_id       TEXT,
            notas_tramitador    TEXT,
            payload_completo    TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def encolar_analisis(response: BertaResponse) -> str:
    """Guarda el análisis de Berta en la cola. Devuelve el id_analisis."""
    conn = _get_conn()
    conn.execute("""
        INSERT INTO cola_validacion
            (id_analisis, expediente_id, codigo_cas, decision_berta, confianza,
             estado_cola, estado_validacion, timestamp_analisis, payload_completo)
        VALUES (?, ?, ?, ?, ?, ?, 'PENDIENTE', ?, ?)
    """, (
        response.id_analisis,
        response.expediente_id,
        response.codigo_cas_recibido,
        response.decision.value,
        response.confianza.value,
        response.estado_cola.value,
        response.timestamp_analisis.isoformat(),
        response.model_dump_json(),
    ))
    conn.commit()
    conn.close()
    return response.id_analisis


def obtener_cola(
    estado: Optional[str] = None,
    limit: int = 50
) -> List[ItemCola]:
    """Lista los elementos de la cola, opcionalmente filtrados por estado."""
    conn = _get_conn()
    if estado:
        rows = conn.execute(
            "SELECT * FROM cola_validacion WHERE estado_validacion = ? ORDER BY timestamp_analisis DESC LIMIT ?",
            (estado, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM cola_validacion ORDER BY timestamp_analisis DESC LIMIT ?",
            (limit,)
        ).fetchall()
    conn.close()

    items = []
    for row in rows:
        items.append(ItemCola(
            id_analisis=row["id_analisis"],
            expediente_id=row["expediente_id"],
            codigo_cas=row["codigo_cas"],
            decision_berta=row["decision_berta"],
            confianza=row["confianza"],
            estado_cola=row["estado_cola"],
            estado_validacion=row["estado_validacion"],
            timestamp_analisis=datetime.fromisoformat(row["timestamp_analisis"]),
            timestamp_validacion=datetime.fromisoformat(row["timestamp_validacion"]) if row["timestamp_validacion"] else None,
            tramitador_id=row["tramitador_id"],
        ))
    return items


def obtener_analisis(id_analisis: str) -> Optional[BertaResponse]:
    """Devuelve el análisis completo de Berta por su ID."""
    conn = _get_conn()
    row = conn.execute(
        "SELECT payload_completo FROM cola_validacion WHERE id_analisis = ?",
        (id_analisis,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    return BertaResponse.model_validate_json(row["payload_completo"])


def validar_analisis(id_analisis: str, validacion: ValidacionHumana) -> bool:
    """Registra la validación humana de un análisis. Devuelve True si existe."""
    conn = _get_conn()
    result = conn.execute(
        """UPDATE cola_validacion
           SET estado_validacion = ?, tramitador_id = ?, notas_tramitador = ?,
               timestamp_validacion = ?
           WHERE id_analisis = ?""",
        (
            validacion.validacion.value,
            validacion.tramitador_id,
            validacion.notas_tramitador,
            datetime.utcnow().isoformat(),
            id_analisis,
        )
    )
    conn.commit()
    updated = result.rowcount > 0
    conn.close()
    return updated


def nueva_id() -> str:
    return str(uuid.uuid4())
