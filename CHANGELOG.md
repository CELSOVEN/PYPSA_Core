# Changelog

## 0.1.1 - 2026-08-07

- Se agrega `requirements.txt` como punto de entrada práctico de instalación.
- `requirements.txt` instala PYPSA Core en modo editable mediante `-e .`.
- Se declara `tzdata` para Windows en `pyproject.toml` como dependencia del paquete.
- Se actualizan las instrucciones de instalación y documentación.

## 0.1.0 - 2026-08-07

- Se crea PYPSA Core como paquete Python con layout `src/`.
- Se incorpora el primer módulo reutilizable: `activity`.
- Se separan las reglas de dominio de Flask y SQLAlchemy.
- Se introduce `ActivityService` con repositorio inyectable.
- Se agregan pruebas unitarias básicas del dominio y del servicio.
