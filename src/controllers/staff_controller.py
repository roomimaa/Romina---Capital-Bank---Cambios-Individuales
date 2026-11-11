"""Controlador del panel de personal."""

from src.controllers.base_controller import BaseController
from src.views.staff_home_view import StaffHomeView
from src.views.view_models import ClienteVista


class StaffController(BaseController):
    requiere_personal = True

    def __init__(self, contexto):
        super().__init__(contexto)
        self.view = None

    def construir(self):
        self.view = StaffHomeView(
            self.page,
            nombre=self.ctx.nombre,
            clientes=self._clientes_vista(),
            on_nuevo=lambda: self.ir("cliente_form"),
            on_ver=lambda dni: self.ir("cliente_form", dni=dni),
            on_logout=self._cerrar_sesion,
        )
        return self.view.build()

    def _clientes_vista(self) -> list[ClienteVista]:
        return [
            ClienteVista(
                dni=cliente.dni,
                nombre_completo=cliente.nombre_completo,
                cuentas=tuple(cuenta.tipo for cuenta in cliente.cuentas),
            )
            for cliente in self.ctx.clientes.listar_clientes()
        ]

    def _cerrar_sesion(self) -> None:
        self.ctx.cerrar_sesion()
        self.ir("login")
