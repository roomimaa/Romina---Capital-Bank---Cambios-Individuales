"""Entidades puras del dominio bancario.

Se reexportan desde aquí para que la capa de modelo tenga un único punto de
entrada, sin mover los archivos históricos que ya usa la suite de tests.

Estas clases no conocen Flet ni SQLAlchemy: solo reglas y estado del negocio.
"""

from src.cliente import Cliente
from src.cuenta import Cuenta, SaldoInsuficienteError
from src.cuenta_ahorro import CuentaAhorro
from src.empleado import Empleado
from src.persona import Persona
from src.transaccion import Transaccion

__all__ = [
    "Cliente",
    "Cuenta",
    "CuentaAhorro",
    "Empleado",
    "Persona",
    "SaldoInsuficienteError",
    "Transaccion",
]
