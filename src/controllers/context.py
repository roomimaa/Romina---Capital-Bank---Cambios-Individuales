"""Contexto de aplicación: dependencias y sesión por pantalla.

Reemplaza el estado global de ``Sesion``: cada ``App`` (cada ``page`` de Flet)
tiene su propio contexto con su usuario autenticado.
"""

from src.models.repositories import DAO
from src.models.services import AuthService, ClientService, OperationService


class AppContext:
    def __init__(self, dao: DAO):
        self.dao = dao
        self.auth = AuthService(dao)
        self.clientes = ClientService(dao)
        self.operaciones = OperationService(dao)
        self.router = None
        self.usuario: dict | None = None

    # ------------------------------------------------------------------
    # Sesión
    # ------------------------------------------------------------------

    def iniciar_sesion(self, usuario: dict) -> None:
        self.usuario = usuario

    def cerrar_sesion(self) -> None:
        self.usuario = None

    @property
    def es_personal(self) -> bool:
        return bool(self.usuario and self.usuario.get("rol") == "personal")

    @property
    def es_cliente(self) -> bool:
        return bool(self.usuario and self.usuario.get("rol") == "cliente")

    @property
    def nombre(self) -> str:
        return self.usuario.get("nombre", "") if self.usuario else ""

    @property
    def cuentas(self) -> list:
        return list(self.usuario.get("cuentas", [])) if self.usuario else []
