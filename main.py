"""Punto de entrada del sistema bancario.

Solo compone las dependencias (base de datos + router) y entrega la ``page``
a la capa de controladores.
"""

from pathlib import Path

import flet as ft

from src.controllers.app import App
from src.models.repositories import DAO

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sistema_bancario.db"


def main(page: ft.Page):
    App(page, DAO(str(DB_PATH))).iniciar()


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)
