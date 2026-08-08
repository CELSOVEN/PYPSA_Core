"""Contratos mínimos que una aplicación debe implementar para usar ActivityService."""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

@runtime_checkable
class SesionActividad(Protocol):
    """Forma mínima de una sesión que PYPSA Core necesita manipular."""
    fecha_salida: Any
    ultima_actividad: Any


@runtime_checkable
class RepositorioActividad(Protocol):
    """Interfaz de persistencia desacoplada de Flask-SQLAlchemy."""

    def crear_sesion(
        self,
        *,
        usuario_id: int,
        nombre_usuario: str,
        username: str,
        direccion_ip: str = "",
        navegador: str = "",
    ) -> SesionActividad:
        ...

    def obtener_sesion(self, registro_id: int) -> SesionActividad | None:
        ...

    def guardar(self, registro: SesionActividad) -> None:
        ...

    def consultar_sesiones(self, *, pagina: int = 1, por_pagina: int = 30) -> Any:
        ...
