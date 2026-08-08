"""Servicios reutilizables de Actividad.

La persistencia se recibe mediante RepositorioActividad. De esta manera el
Core no importa database.py, models.py, Flask ni SQLAlchemy de Project Hub.
"""
from __future__ import annotations

from collections.abc import Callable
from datetime import datetime

from .contracts import RepositorioActividad
from .domain import INTERVALO_ACTUALIZACION_SEGUNDOS, utcnow_naive


class ActivityService:
    """Orquesta registro, cierre, refresco y consulta de sesiones."""

    def __init__(
        self,
        repositorio: RepositorioActividad,
        *,
        reloj: Callable[[], datetime] = utcnow_naive,
        intervalo_actualizacion_segundos: int = INTERVALO_ACTUALIZACION_SEGUNDOS,
    ) -> None:
        self.repositorio = repositorio
        self.reloj = reloj
        self.intervalo_actualizacion_segundos = intervalo_actualizacion_segundos

    def registrar_ingreso(
        self,
        *,
        usuario_id: int,
        nombre_usuario: str,
        username: str,
        direccion_ip: str = "",
        navegador: str = "",
    ):
        """Crea una nueva sesión de navegación."""
        return self.repositorio.crear_sesion(
            usuario_id=usuario_id,
            nombre_usuario=nombre_usuario,
            username=username,
            direccion_ip=direccion_ip,
            navegador=(navegador or "")[:255],
        )

    def cerrar_sesion(self, registro_id):
        """Marca una sesión abierta como cerrada."""
        if not registro_id:
            return None

        registro = self.repositorio.obtener_sesion(registro_id)
        if registro and not registro.fecha_salida:
            ahora = self.reloj()
            registro.fecha_salida = ahora
            registro.ultima_actividad = ahora
            self.repositorio.guardar(registro)
        return registro

    def actualizar_ultima_actividad(self, registro_id):
        """Refresca última actividad sólo cuando transcurrió el intervalo configurado."""
        if not registro_id:
            return None

        registro = self.repositorio.obtener_sesion(registro_id)
        if registro and not registro.fecha_salida:
            ahora = self.reloj()
            if (ahora - registro.ultima_actividad).total_seconds() >= self.intervalo_actualizacion_segundos:
                registro.ultima_actividad = ahora
                self.repositorio.guardar(registro)
        return registro

    def consultar_sesiones(self, *, pagina: int = 1, por_pagina: int = 30):
        """Delega al repositorio la consulta paginada de sesiones."""
        return self.repositorio.consultar_sesiones(pagina=pagina, por_pagina=por_pagina)
