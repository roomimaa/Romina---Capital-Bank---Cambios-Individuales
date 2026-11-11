"""Punto de entrada del sistema bancario.

Solo compone las dependencias (base de datos + router) y entrega la ``page``
a la capa de controladores.

Configuracion por variables de entorno (util para Docker):

- ``DB_PATH``: ruta del archivo SQLite (por defecto ``sistema_bancario.db``).
- ``FLET_SERVER_IP``: host donde escucha el servidor web (por defecto ``127.0.0.1``).
- ``FLET_SERVER_PORT``: puerto del servidor web (por defecto ``8550``).
- ``FLET_FORCE_WEB_SERVER``: si es ``true``, fuerza modo servidor web sin navegador.
"""

import os
from pathlib import Path

import flet as ft

from src.controllers.app import App
from src.models.repositories import DAO

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("DB_PATH", str(BASE_DIR / "sistema_bancario.db")))

SERVER_HOST = os.getenv("FLET_SERVER_IP", "127.0.0.1")
SERVER_PORT = int(os.getenv("FLET_SERVER_PORT", "8550"))


def main(page: ft.Page):
    App(page, DAO(str(DB_PATH))).iniciar()


if __name__ == "__main__":
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        host=SERVER_HOST,
        port=SERVER_PORT,
    )
