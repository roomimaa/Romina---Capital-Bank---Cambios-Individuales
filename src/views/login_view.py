"""Vista de login. Solo dibuja y avisa cuando el usuario hace clic."""

import base64
from pathlib import Path

import flet as ft

from src.views import theme
from src.views.components import mostrar_snack

_LOGO = Path(__file__).resolve().parents[2] / "img" / "logo_clean.png"


def _logo_src() -> str:
    if not _LOGO.exists():
        return ""
    datos = base64.b64encode(_LOGO.read_bytes()).decode()
    return "data:image/png;base64," + datos


class LoginView:
    def __init__(self, page: ft.Page, on_login):
        self.page = page
        self.on_login = on_login

        self.dni = ft.TextField(
            label="DNI",
            label_style=ft.TextStyle(color=theme.TEXTO_SUAVE),
            hint_text="Sin puntos, ej. 40345678",
            hint_style=ft.TextStyle(color=theme.TEXTO_OSCURO),
            text_style=ft.TextStyle(color=theme.BLANCO),
            bgcolor="#121212",
            border_color="#8b2fc9",
            focused_border_color=theme.VIOLETA_CLARO,
            border_radius=25,
            content_padding=ft.Padding(20, 12, 20, 12),
            text_align=ft.TextAlign.CENTER,
        )

        self.clave = ft.TextField(
            label="Clave",
            label_style=ft.TextStyle(color=theme.TEXTO_SUAVE),
            hint_text="Tu clave",
            password=True,
            can_reveal_password=True,
            hint_style=ft.TextStyle(color=theme.TEXTO_OSCURO),
            text_style=ft.TextStyle(color=theme.BLANCO),
            bgcolor="#121212",
            border_color="#8b2fc9",
            focused_border_color=theme.VIOLETA_CLARO,
            border_radius=25,
            content_padding=ft.Padding(20, 12, 20, 12),
            text_align=ft.TextAlign.CENTER,
        )

    def build(self) -> ft.Control:
        self._configurar_pagina()

        btn_ingresar = ft.Button(
            content=ft.Text(
                "INGRESAR",
                size=15,
                weight=ft.FontWeight.BOLD,
                color=theme.BLANCO,
            ),
            on_click=self._click_ingresar,
            style=ft.ButtonStyle(
                bgcolor="#8b2fc9",
                padding=ft.Padding(0, 15, 0, 15),
                shape=ft.RoundedRectangleBorder(radius=25),
                elevation=5,
            ),
            width=300,
        )

        btn_olvido = ft.TextButton(
            content=ft.Text(
                "¿Olvidaste tu clave?",
                size=12,
                color=theme.VIOLETA_CLARO,
            ),
            on_click=lambda _: self.mostrar_mensaje(
                "Contacta a soporte técnico", error=False
            ),
        )

        tarjeta = ft.Container(
            width=340,
            padding=30,
            bgcolor="#181820",
            border_radius=20,
            border=ft.border.all(1, theme.LINEA),
            shadow=ft.BoxShadow(
                blur_radius=25,
                color="#8b2fc9",
                offset=ft.Offset(0, 0),
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=18,
                controls=[
                    ft.Container(
                        content=ft.Image(
                            src=_logo_src() or str(_LOGO),
                            width=140,
                            height=140,
                            fit="contain",
                        ),
                        alignment=ft.Alignment(0, 0),
                        width=280,
                    ),
                    ft.Container(height=2),
                    ft.Text(
                        "Ingresá con tu DNI para ver tus cuentas",
                        size=13,
                        color=theme.TEXTO_SUAVE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    self.dni,
                    self.clave,
                    ft.Container(height=2),
                    btn_ingresar,
                    btn_olvido,
                    ft.Text(
                        "Personal: DNI 22233344 / clave admin123",
                        size=11,
                        color=theme.TEXTO_OSCURO,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )

        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=25,
            controls=[
                tarjeta,
                ft.Text(
                    "© 2026 Capital Bank • Sistema Bancario Seguro",
                    size=11,
                    color="#555566",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        )

    def _configurar_pagina(self) -> None:
        self.page.title = "Capital Bank - Login"
        self.page.window_width = 420
        self.page.window_height = 680
        self.page.window_resizable = False
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.bgcolor = "#0a0a0f"
        self.page.scroll = ft.ScrollMode.ADAPTIVE

    def _click_ingresar(self, _evento) -> None:
        self.on_login(self.dni.value or "", self.clave.value or "")

    def mostrar_mensaje(self, texto: str, error: bool = False) -> None:
        mostrar_snack(self.page, texto, error)

    def limpiar_clave(self) -> None:
        self.clave.value = ""
        self.page.update()
