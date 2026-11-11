"""Composición raíz y router de la aplicación.

``App`` es el único punto que conoce a todos los controladores. Se encarga de:

- crear el contexto con el DAO y los servicios,
- construir el controlador de cada ruta,
- aplicar las guardas de sesión (personal / cliente),
- montar la vista resultante en la ``page`` de Flet.

Los controladores no se importan entre sí: piden navegación a ``App`` a través
de ``AppContext.router``.
"""

import flet as ft

from src.controllers.client_controller import ClientHomeController
from src.controllers.client_form_controller import ClientFormController
from src.controllers.context import AppContext
from src.controllers.history_controller import HistoryController
from src.controllers.login_controller import LoginController
from src.controllers.operations_controller import OperationsController
from src.controllers.staff_controller import StaffController
from src.models.repositories import DAO
from src.views.components import mostrar_snack


class App:
    """Router y composición raíz del sistema bancario."""

    def __init__(self, page: ft.Page, dao: DAO):
        self.page = page
        self.ctx = AppContext(dao)
        self.ctx.router = self

        self._rutas = {
            "login": self._crear_login,
            "home_cliente": self._crear_home_cliente,
            "operaciones": self._crear_operaciones,
            "historial": self._crear_historial,
            "home_personal": self._crear_home_personal,
            "cliente_form": self._crear_cliente_form,
        }

    # ------------------------------------------------------------------
    # Navegación
    # ------------------------------------------------------------------

    def iniciar(self) -> None:
        self.ir("login")

    def ir(
        self,
        ruta: str,
        mensaje: str | None = None,
        error: bool = False,
        **kwargs,
    ) -> None:
        """Construye la ruta pedida, aplica guardas y monta la vista."""
        fabrica = self._rutas.get(ruta)
        if fabrica is None:
            raise ValueError(f"Ruta desconocida: {ruta}")

        controlador = fabrica(**kwargs)

        if not self._autorizado(controlador):
            self.ctx.cerrar_sesion()
            self.ir(
                "login",
                mensaje="Iniciá sesión para continuar.",
                error=True,
            )
            return

        control = controlador.construir()

        # Si el controlador redirigió (por ejemplo, cliente inexistente),
        # ya montó la pantalla destino y devuelve None: no hay que tocarla.
        if control is None:
            return

        self.page.clean()
        self.page.add(control)
        self.page.update()

        if mensaje:
            mostrar_snack(self.page, mensaje, error)

    @staticmethod
    def _autorizado(controlador) -> bool:
        if controlador.requiere_personal:
            return controlador.ctx.es_personal
        if controlador.requiere_cliente:
            return controlador.ctx.es_cliente
        return True

    # ------------------------------------------------------------------
    # Factorías de controladores (evitan imports cruzados entre ellos)
    # ------------------------------------------------------------------

    def _crear_login(self, **_kwargs) -> LoginController:
        return LoginController(self.ctx)

    def _crear_home_cliente(self, **_kwargs) -> ClientHomeController:
        return ClientHomeController(self.ctx)

    def _crear_operaciones(self, **_kwargs) -> OperationsController:
        return OperationsController(self.ctx)

    def _crear_historial(self, **_kwargs) -> HistoryController:
        return HistoryController(self.ctx)

    def _crear_home_personal(self, **_kwargs) -> StaffController:
        return StaffController(self.ctx)

    def _crear_cliente_form(
        self, dni: str | None = None, **_kwargs
    ) -> ClientFormController:
        return ClientFormController(self.ctx, dni=dni)
