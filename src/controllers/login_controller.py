"""Controlador del login: valida, inicia sesión y navega."""

from src.controllers.base_controller import BaseController
from src.views.login_view import LoginView


class LoginController(BaseController):
    def __init__(self, contexto):
        super().__init__(contexto)
        self.view = LoginView(self.page, on_login=self._iniciar_sesion)

    def construir(self):
        return self.view.build()

    def _iniciar_sesion(self, dni: str, clave: str) -> None:
        try:
            usuario = self.ctx.auth.autenticar(dni, clave)
        except ValueError as error:
            self.view.mostrar_mensaje(str(error), error=True)
            return
        except Exception:
            self.view.mostrar_mensaje(
                "Ocurrió un error inesperado. Intentá nuevamente.",
                error=True,
            )
            return

        if usuario is None:
            self.view.mostrar_mensaje("DNI o clave incorrectos.", error=True)
            return

        self.ctx.iniciar_sesion(usuario)
        destino = "home_personal" if usuario["rol"] == "personal" else "home_cliente"
        self.ir(destino)
