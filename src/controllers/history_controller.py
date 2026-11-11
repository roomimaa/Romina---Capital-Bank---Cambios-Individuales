"""Controlador del historial: prepara movimientos y aplica filtros."""

from src.controllers.base_controller import BaseController
from src.views.formatting import etiqueta_operacion, formatear_fecha
from src.views.history_view import HistoryView
from src.views.view_models import MovimientoVista


class HistoryController(BaseController):
    requiere_cliente = True

    def __init__(self, contexto):
        super().__init__(contexto)
        self.view = None
        self._movimientos = []

    def construir(self):
        self._movimientos = self.ctx.operaciones.historial(self.ctx.cuentas)
        filtros = sorted({movimiento.cuenta for movimiento in self._movimientos})

        self.view = HistoryView(
            self.page,
            nombre=self.ctx.nombre,
            movimientos=self._a_vista(self._movimientos),
            filtros=filtros,
            on_filtrar=self._filtrar,
            on_nav_inicio=lambda: self.ir("home_cliente"),
            on_nav_operar=lambda: self.ir("operaciones"),
            on_nav_historial=lambda: self.ir("historial"),
            on_logout=self._cerrar_sesion,
        )
        return self.view.build()

    def _filtrar(self, etiqueta: str) -> None:
        if etiqueta == "Todas":
            seleccionados = self._movimientos
        else:
            seleccionados = [
                movimiento
                for movimiento in self._movimientos
                if movimiento.cuenta == etiqueta
            ]
        self.view.actualizar_movimientos(self._a_vista(seleccionados))

    @staticmethod
    def _a_vista(movimientos) -> list[MovimientoVista]:
        return [
            MovimientoVista(
                fecha=formatear_fecha(movimiento.fecha),
                operacion=etiqueta_operacion(movimiento.tipo),
                cuenta=movimiento.cuenta,
                monto=movimiento.monto,
            )
            for movimiento in movimientos
        ]

    def _cerrar_sesion(self) -> None:
        self.ctx.cerrar_sesion()
        self.ir("login")
