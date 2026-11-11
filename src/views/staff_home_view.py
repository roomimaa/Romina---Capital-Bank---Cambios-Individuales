"""Vista del panel de personal. Solo dibuja la tabla de clientes."""

import flet as ft

from src.views import theme
from src.views.components import mostrar_snack
from src.views.view_models import ClienteVista


class StaffHomeView:
    def __init__(
        self,
        page: ft.Page,
        nombre: str,
        clientes: list[ClienteVista],
        on_nuevo,
        on_ver,
        on_logout,
    ):
        self.page = page
        self.nombre = nombre
        self.clientes = clientes
        self.on_nuevo = on_nuevo
        self.on_ver = on_ver
        self.on_logout = on_logout

    def build(self) -> ft.Control:
        self._configurar_pagina()

        filas = [self._fila(cliente) for cliente in self.clientes]
        if not filas:
            filas.append(
                ft.Container(
                    padding=40,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text(
                        "No hay clientes registrados en el sistema.",
                        size=13,
                        color=theme.TEXTO_SUAVE,
                    ),
                )
            )

        tabla = ft.Container(
            bgcolor="#121118",
            border_radius=18,
            border=ft.border.all(1.5, theme.BORDE_NEON),
            shadow=ft.BoxShadow(
                blur_radius=18,
                color="#581c87",
                offset=ft.Offset(0, 0),
            ),
            content=ft.Column(
                spacing=0,
                controls=[
                    self._cabecera_tabla(),
                    ft.Container(height=1, bgcolor="#232130"),
                    ft.Column(
                        spacing=0,
                        scroll=ft.ScrollMode.ADAPTIVE,
                        controls=filas,
                    ),
                ],
            ),
        )

        return ft.Container(
            padding=ft.Padding(36, 28, 36, 28),
            expand=True,
            content=ft.Column(
                expand=True,
                spacing=24,
                controls=[self._header(), tabla],
            ),
        )

    def _configurar_pagina(self) -> None:
        self.page.title = "Capital Bank - Personal"
        self.page.window_width = 980
        self.page.window_height = 640
        self.page.window_resizable = True
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.bgcolor = "#0c0b11"

    def _header(self) -> ft.Row:
        logo = ft.Row(
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=46,
                    height=52,
                    border_radius=8,
                    border=ft.border.all(2, theme.VIOLETA_CLARO),
                    shadow=ft.BoxShadow(
                        blur_radius=12,
                        color=theme.BORDE_NEON,
                        offset=ft.Offset(0, 0),
                    ),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=1,
                        controls=[
                            ft.Icon(
                                ft.Icons.SHIELD_OUTLINED,
                                color=theme.VIOLETA_CLARO,
                                size=24,
                            ),
                            ft.Text(
                                "CB",
                                size=9,
                                weight=ft.FontWeight.BOLD,
                                color=theme.VIOLETA_CLARO,
                            ),
                        ],
                    ),
                ),
                ft.Column(
                    spacing=0,
                    controls=[
                        ft.Text(
                            "CAPITAL",
                            size=13,
                            weight=ft.FontWeight.BOLD,
                            color=theme.BLANCO,
                        ),
                        ft.Text(
                            "BANK",
                            size=13,
                            weight=ft.FontWeight.BOLD,
                            color=theme.BLANCO,
                        ),
                    ],
                ),
            ],
        )

        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=24,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        logo,
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(
                                    "VISTA PERSONAL",
                                    size=11,
                                    weight=ft.FontWeight.BOLD,
                                    color=theme.VIOLETA_CLARO,
                                ),
                                ft.Text(
                                    "Clientes",
                                    size=32,
                                    weight=ft.FontWeight.BOLD,
                                    color=theme.BLANCO,
                                ),
                                ft.Text(
                                    "Dale de alta a los clientes y a sus cuentas",
                                    size=13,
                                    color=theme.TEXTO_SUAVE,
                                ),
                            ],
                        ),
                    ],
                ),
                ft.Row(
                    spacing=12,
                    controls=[
                        ft.ElevatedButton(
                            content=ft.Text(
                                "+ Alta cliente",
                                size=14,
                                weight=ft.FontWeight.W_600,
                                color=theme.BLANCO,
                            ),
                            bgcolor=theme.BORDE_NEON,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                padding=ft.Padding(20, 14, 20, 14),
                                shadow_color=theme.VIOLETA_CLARO,
                                elevation=6,
                            ),
                            on_click=lambda _e: self.on_nuevo(),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.LOGOUT_ROUNDED,
                            icon_color=theme.TEXTO_SUAVE,
                            icon_size=20,
                            tooltip="Cerrar sesión",
                            on_click=lambda _e: self.on_logout(),
                        ),
                    ],
                ),
            ],
        )

    @staticmethod
    def _cabecera_tabla() -> ft.Container:
        def columna(texto: str, expand: int, derecha: bool = False) -> ft.Container:
            return ft.Container(
                expand=expand,
                alignment=ft.Alignment(1, 0) if derecha else None,
                content=ft.Text(
                    texto,
                    size=11,
                    weight=ft.FontWeight.BOLD,
                    color=theme.TEXTO_SUAVE,
                ),
            )

        return ft.Container(
            padding=ft.Padding(24, 16, 24, 12),
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    columna("CLIENTE", 3),
                    columna("DNI", 2),
                    columna("CUENTAS", 3),
                    columna("ACCIÓN", 1, derecha=True),
                ],
            ),
        )

    def _fila(self, cliente: ClienteVista) -> ft.Container:
        badges = [
            ft.Container(
                padding=ft.Padding(10, 4, 10, 4),
                border=ft.border.all(1, theme.VIOLETA_CLARO),
                border_radius=8,
                content=ft.Text(
                    etiqueta,
                    size=11,
                    color=theme.BLANCO,
                ),
            )
            for etiqueta in cliente.cuentas
        ] or [
            ft.Text(
                "Sin cuentas",
                size=11,
                color=theme.TEXTO_SUAVE,
            )
        ]

        return ft.Container(
            padding=ft.Padding(24, 14, 24, 14),
            border=ft.Border(bottom=ft.BorderSide(1, "#232130")),
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        expand=3,
                        content=ft.Text(
                            cliente.nombre_completo,
                            size=14,
                            weight=ft.FontWeight.W_500,
                            color=theme.BLANCO,
                        ),
                    ),
                    ft.Container(
                        expand=2,
                        content=ft.Text(
                            cliente.dni,
                            size=14,
                            color=theme.BLANCO,
                        ),
                    ),
                    ft.Container(
                        expand=3,
                        content=ft.Row(wrap=True, spacing=6, controls=badges),
                    ),
                    ft.Container(
                        expand=1,
                        alignment=ft.Alignment(1, 0),
                        content=ft.OutlinedButton(
                            content=ft.Text(
                                "Ver",
                                size=12,
                                color=theme.BLANCO,
                            ),
                            style=ft.ButtonStyle(
                                side=ft.BorderSide(1, theme.VIOLETA_CLARO),
                                shape=ft.RoundedRectangleBorder(radius=10),
                                padding=ft.Padding(18, 8, 18, 8),
                            ),
                            on_click=lambda _e, d=cliente.dni: self.on_ver(d),
                        ),
                    ),
                ],
            ),
        )

    def mostrar_mensaje(self, texto: str, error: bool = False) -> None:
        mostrar_snack(self.page, texto, error)
