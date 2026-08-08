"""Reglas de dominio reutilizables para el seguimiento de actividad.

Este módulo no depende de Flask, SQLAlchemy ni de una aplicación concreta.
Las aplicaciones pueden reutilizar estas reglas con su propia persistencia,
autenticación, permisos e interfaz.
"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

ZONA_HORARIA_DEFAULT = "America/Mexico_City"
MINUTOS_INACTIVIDAD_DEFAULT = 30
INTERVALO_ACTUALIZACION_SEGUNDOS = 60


def utcnow_naive() -> datetime:
    """Devuelve UTC sin tzinfo para compatibilidad con BD que guardan DateTime naive."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def calcular_duracion_segundos(fecha_ingreso, fecha_salida, ultima_actividad) -> int:
    """Calcula la duración de una sesión usando la salida o la última actividad."""
    fin = fecha_salida or ultima_actividad
    if not fecha_ingreso or not fin:
        return 0
    return max(0, int((fin - fecha_ingreso).total_seconds()))


def sesion_esta_activa(
    fecha_salida,
    ultima_actividad,
    *,
    ahora=None,
    minutos_inactividad: int = MINUTOS_INACTIVIDAD_DEFAULT,
) -> bool:
    """Indica si una sesión sigue activa dentro de la ventana de inactividad."""
    if fecha_salida or not ultima_actividad:
        return False
    ahora = ahora or utcnow_naive()
    limite = ahora - timedelta(minutes=minutos_inactividad)
    return ultima_actividad >= limite


def obtener_estado_sesion(fecha_salida, ultima_actividad, *, ahora=None) -> str:
    """Devuelve el estado de sesión usado por las aplicaciones PYPSA."""
    if fecha_salida:
        return "Cerrada"
    if sesion_esta_activa(fecha_salida, ultima_actividad, ahora=ahora):
        return "En curso"
    return "Inactiva..."


def formatear_fecha_hora(valor, zona_horaria: str = ZONA_HORARIA_DEFAULT) -> str:
    """Convierte fechas UTC naive a una zona horaria local y las formatea."""
    if not valor:
        return "—"

    zona_local = ZoneInfo(zona_horaria)
    if valor.tzinfo is None:
        valor = valor.replace(tzinfo=timezone.utc)
    valor = valor.astimezone(zona_local)
    return valor.strftime("%d/%m/%Y %H:%M")


def formatear_duracion(segundos) -> str:
    """Formatea una duración en segundos como HH:MM:SS."""
    segundos = max(0, int(segundos or 0))
    horas, resto = divmod(segundos, 3600)
    minutos, segundos = divmod(resto, 60)
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
