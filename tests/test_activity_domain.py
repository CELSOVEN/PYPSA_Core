from datetime import datetime, timedelta
import unittest

from pypsa_core.activity import (
    calcular_duracion_segundos,
    formatear_duracion,
    formatear_fecha_hora,
    obtener_estado_sesion,
    sesion_esta_activa,
)


class ActivityDomainTests(unittest.TestCase):
    def test_duracion_prefiere_fecha_salida(self):
        inicio = datetime(2026, 8, 7, 12, 0, 0)
        ultima = datetime(2026, 8, 7, 12, 20, 0)
        salida = datetime(2026, 8, 7, 12, 30, 0)
        self.assertEqual(calcular_duracion_segundos(inicio, salida, ultima), 1800)

    def test_sesion_en_curso_dentro_de_30_minutos(self):
        ahora = datetime(2026, 8, 7, 15, 0, 0)
        ultima = ahora - timedelta(minutes=29)
        self.assertTrue(sesion_esta_activa(None, ultima, ahora=ahora))
        self.assertEqual(obtener_estado_sesion(None, ultima, ahora=ahora), "En curso")

    def test_sesion_inactiva_fuera_de_30_minutos(self):
        ahora = datetime(2026, 8, 7, 15, 0, 0)
        ultima = ahora - timedelta(minutes=31)
        self.assertFalse(sesion_esta_activa(None, ultima, ahora=ahora))
        self.assertEqual(obtener_estado_sesion(None, ultima, ahora=ahora), "Inactiva...")

    def test_sesion_cerrada(self):
        ahora = datetime(2026, 8, 7, 15, 0, 0)
        self.assertEqual(obtener_estado_sesion(ahora, ahora, ahora=ahora), "Cerrada")

    def test_formato_duracion(self):
        self.assertEqual(formatear_duracion(3661), "01:01:01")

    def test_fecha_utc_naive_a_mexico(self):
        valor = datetime(2026, 8, 7, 15, 0, 0)
        self.assertEqual(formatear_fecha_hora(valor), "07/08/2026 09:00")


if __name__ == "__main__":
    unittest.main()
