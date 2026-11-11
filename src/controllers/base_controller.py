"""Controlador base: contrato común de todos los mediadores."""

from abc import ABC, abstractmethod

import flet as ft


class BaseController(ABC):
    # Guardas declarativas: la app redirige si no se cumplen.
    requiere_personal = False
    requiere_cliente = False

    def __init__(self, contexto):
        self.ctx = contexto
        self.page: ft.Page = contexto.router.page

    @abstractmethod
    def construir(self) -> ft.Control | None:
        """Arma la vista y devuelve el control raíz (o None si redirigió)."""

    def ir(self, ruta: str, **kwargs) -> None:
        self.ctx.router.ir(ruta, **kwargs)
