"""Datos ya preparados que la vista puede dibujar.

La vista no conoce las entidades del dominio ni la base de datos: recibe
objetos simples armados por el controlador.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CuentaVista:
    id_cuenta: int
    numero: str
    tipo: str
    saldo: float


@dataclass(frozen=True)
class ClienteVista:
    dni: str
    nombre_completo: str
    cuentas: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class MovimientoVista:
    fecha: str
    operacion: str
    cuenta: str
    monto: float


@dataclass(frozen=True)
class ClienteFormVista:
    nombre: str
    apellido: str
    dni: str
