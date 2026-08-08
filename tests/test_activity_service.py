from dataclasses import dataclass
from datetime import datetime, timedelta
import unittest

from pypsa_core.activity import ActivityService


@dataclass
class RegistroFake:
    id: int
    usuario_id: int
    nombre_usuario: str
    username: str
    fecha_ingreso: datetime
    ultima_actividad: datetime
    fecha_salida: datetime | None = None
    direccion_ip: str = ""
    navegador: str = ""


class RepositorioFake:
    def __init__(self, ahora):
        self.ahora = ahora
        self.registros = {}
        self.guardados = 0

    def crear_sesion(self, *, usuario_id, nombre_usuario, username, direccion_ip="", navegador=""):
        registro = RegistroFake(
            id=len(self.registros) + 1,
            usuario_id=usuario_id,
            nombre_usuario=nombre_usuario,
            username=username,
            fecha_ingreso=self.ahora,
            ultima_actividad=self.ahora,
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
        self.registros[registro.id] = registro
        return registro

    def obtener_sesion(self, registro_id):
        return self.registros.get(registro_id)

    def guardar(self, registro):
        self.registros[registro.id] = registro
        self.guardados += 1

    def consultar_sesiones(self, *, pagina=1, por_pagina=30):
        return list(self.registros.values())


class ActivityServiceTests(unittest.TestCase):
    def test_registrar_y_cerrar_sesion(self):
        ahora = datetime(2026, 8, 7, 15, 0, 0)
        repo = RepositorioFake(ahora)
        servicio = ActivityService(repo, reloj=lambda: ahora)

        registro = servicio.registrar_ingreso(
            usuario_id=1,
            nombre_usuario="Celso Montiel",
            username="administrator",
            direccion_ip="127.0.0.1",
            navegador="Browser",
        )
        self.assertEqual(registro.username, "administrator")
        self.assertIsNone(registro.fecha_salida)

        servicio.cerrar_sesion(registro.id)
        self.assertEqual(registro.fecha_salida, ahora)
        self.assertEqual(registro.ultima_actividad, ahora)
        self.assertEqual(repo.guardados, 1)

    def test_actualizacion_respetando_intervalo(self):
        ingreso = datetime(2026, 8, 7, 15, 0, 0)
        ahora = ingreso + timedelta(seconds=61)
        repo = RepositorioFake(ingreso)
        registro = repo.crear_sesion(usuario_id=1, nombre_usuario="Celso", username="admin")
        servicio = ActivityService(repo, reloj=lambda: ahora)

        servicio.actualizar_ultima_actividad(registro.id)
        self.assertEqual(registro.ultima_actividad, ahora)
        self.assertEqual(repo.guardados, 1)


if __name__ == "__main__":
    unittest.main()
