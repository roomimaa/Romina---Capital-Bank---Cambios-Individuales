"""Capa de MODELO del sistema bancario.

Este paquete es la fachada pública del modelo y agrupa:

- ``orm``: mapeo de las tablas con SQLAlchemy.
- ``repositories``: acceso a datos (DAO). Es la única capa que habla SQL.
- ``entities``: entidades puras del dominio (sin Flet y sin SQL).
- ``services``: reglas de negocio; orquestan repositorios y entidades.

Ningún módulo de este paquete importa Flet.
"""

from src.models.entities import (
    Cliente,
    Cuenta,
    CuentaAhorro,
    Empleado,
    Persona,
    SaldoInsuficienteError,
    Transaccion,
)
from src.models.orm import (
    Base,
    ClienteModel,
    CuentaModel,
    EmpleadoModel,
    PersonaModel,
    TipoCuentaModel,
    TipoTransaccionModel,
    TransaccionModel,
)
from src.models.repositories import DAO, pwd_context

__all__ = [
    "Base",
    "Cliente",
    "ClienteModel",
    "Cuenta",
    "CuentaAhorro",
    "CuentaModel",
    "DAO",
    "Empleado",
    "EmpleadoModel",
    "Persona",
    "PersonaModel",
    "SaldoInsuficienteError",
    "TipoCuentaModel",
    "TipoTransaccionModel",
    "Transaccion",
    "TransaccionModel",
    "pwd_context",
]
