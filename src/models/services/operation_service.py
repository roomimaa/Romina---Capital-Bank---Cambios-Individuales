"""Servicio de operaciones bancarias e historial.

Aplica las reglas del dominio (Cuenta) y persiste a través del repositorio.
No conoce Flet.
"""

from dataclasses import dataclass
from datetime import datetime

from src.models.entities import Cuenta
from src.models.repositories import DAO
from src.models.services.validaciones import parsear_monto


@dataclass(frozen=True)
class Movimiento:
    fecha: datetime
    tipo: str
    cuenta: str
    monto: float

    @property
    def es_deposito(self) -> bool:
        return self.tipo == "deposito"


class OperationService:
    """Depósitos, retiros e historial de las cuentas del cliente."""

    def __init__(self, dao: DAO):
        self.dao = dao

    def depositar(self, cuenta: Cuenta, monto_texto) -> float:
        monto = parsear_monto(monto_texto)
        cuenta.depositar(monto)
        self._persistir(cuenta, "deposito", monto)
        return cuenta.get_saldo()

    def retirar(self, cuenta: Cuenta, monto_texto) -> float:
        monto = parsear_monto(monto_texto)
        cuenta.retirar(monto)
        self._persistir(cuenta, "retiro", monto)
        return cuenta.get_saldo()

    def historial(self, cuentas) -> list[Movimiento]:
        cuentas = list(cuentas or [])
        if not cuentas:
            return []

        etiquetas = {
            cuenta.get_id_cuenta(): self.etiqueta_cuenta(cuenta)
            for cuenta in cuentas
        }
        filas = self.dao.listar_transacciones(
            [cuenta.get_id_cuenta() for cuenta in cuentas]
        )

        movimientos = []
        for fila in filas:
            es_deposito = fila["tipo"] == "deposito"
            movimientos.append(
                Movimiento(
                    fecha=fila["fecha"],
                    tipo=fila["tipo"],
                    cuenta=etiquetas.get(fila["id_cuenta"], "Cuenta"),
                    monto=fila["monto"] if es_deposito else -fila["monto"],
                )
            )
        return movimientos

    def etiqueta_cuenta(self, cuenta: Cuenta) -> str:
        nombre_tipo = self.dao.listar_tipos_cuenta().get(
            cuenta.get_id_tipo_cuenta(), ""
        )
        if "ahorro" in nombre_tipo.lower():
            return "Caja de ahorro"
        return nombre_tipo or "Cuenta"

    @staticmethod
    def total_saldos(cuentas) -> float:
        """Suma de saldos: la vista recibe el total ya calculado."""
        return sum(cuenta.get_saldo() for cuenta in cuentas)

    def _persistir(self, cuenta: Cuenta, tipo: str, monto: float) -> None:
        ok = self.dao.registrar_movimiento(
            cuenta.get_id_cuenta(),
            cuenta.get_saldo(),
            tipo,
            monto,
        )
        if not ok:
            raise RuntimeError(
                "No se pudo guardar la operación en la base de datos."
            )
