"""Controlador de operaciones: intercepta el clic y delega en el servicio."""

from src.controllers.base_controller import BaseController
from src.models.entities import SaldoInsuficienteError
from src.views.formatting import formatear_monto
from src.views.operations_view import OperationsView
from src.views.view_models import CuentaVista


class OperationsController(BaseController):
    requiere_cliente = True

    def __init__(self, contexto):
        super().__init__(contexto)
        self.view = None

    def construir(self):
        self.view = OperationsView(
            self.page,
            nombre=self.ctx.nombre,
            cuentas=self._cuentas_vista(),
            on_ejecutar=self._ejecutar,
            on_nav_inicio=lambda: self.ir("home_cliente"),
            on_nav_operar=lambda: self.ir("operaciones"),
            on_nav_historial=lambda: self.ir("historial"),
        )
        return self.view.build()

    def _cuentas_vista(self) -> list[CuentaVista]:
        return [
            CuentaVista(
                id_cuenta=cuenta.get_id_cuenta(),
                numero=cuenta.get_nro_cuenta(),
                tipo=self.ctx.operaciones.etiqueta_cuenta(cuenta),
                saldo=cuenta.get_saldo(),
            )
            for cuenta in self.ctx.cuentas
        ]

    def _ejecutar(self, id_cuenta: int, tipo: str, monto_texto: str) -> None:
        cuenta = next(
            (
                cuenta
                for cuenta in self.ctx.cuentas
                if cuenta.get_id_cuenta() == id_cuenta
            ),
            None,
        )
        if cuenta is None:
            self.view.mostrar_mensaje(
                "La cuenta seleccionada no existe.", error=True
            )
            return

        try:
            if tipo == "deposito":
                saldo = self.ctx.operaciones.depositar(cuenta, monto_texto)
                etiqueta = "Depósito"
            else:
                saldo = self.ctx.operaciones.retirar(cuenta, monto_texto)
                etiqueta = "Retiro"
        except (ValueError, SaldoInsuficienteError) as error:
            self.view.mostrar_mensaje(str(error), error=True)
            return
        except Exception:
            self.view.mostrar_mensaje(
                "No se pudo completar la operación. Intentá nuevamente.",
                error=True,
            )
            return

        self.view.limpiar_monto()
        self.view.mostrar_mensaje(
            f"{etiqueta} realizado. Saldo actual: {formatear_monto(saldo)}"
        )
