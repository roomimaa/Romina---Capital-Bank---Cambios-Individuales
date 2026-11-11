"""Controlador del home del cliente."""

from src.controllers.base_controller import BaseController
from src.views.client_home_view import ClientHomeView
from src.views.view_models import CuentaVista


class ClientHomeController(BaseController):
    requiere_cliente = True

    def __init__(self, contexto):
        super().__init__(contexto)
        self.view = None

    def construir(self):
        self.view = ClientHomeView(
            self.page,
            nombre=self.ctx.nombre,
            cuentas=self._cuentas_vista(),
            total=self.ctx.operaciones.total_saldos(self.ctx.cuentas),
            on_logout=self._cerrar_sesion,
            on_inicio=lambda: self.ir("home_cliente"),
            on_operar=lambda: self.ir("operaciones"),
            on_historial=lambda: self.ir("historial"),
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

    def _cerrar_sesion(self) -> None:
        self.ctx.cerrar_sesion()
        self.ir("login")
