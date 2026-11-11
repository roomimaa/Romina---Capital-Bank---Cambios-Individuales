"""Vista del historial. Recibe movimientos ya calculados por el controlador."""

import flet as ft

from src.views import theme
from src.views.components import barra_navegacion
from src.views.formatting import formatear_monto_movimiento
from src.views.view_models import MovimientoVista


class HistoryView:
    def __init__(
        self,
        page: ft.Page,
        nombre: str,
        movimientos: list[MovimientoVista],
        filtros: list[str],
        on_filtrar,
        on_nav_inicio,
        on_nav_operar,
        on_nav_historial,
        on_logout,
    ):
        self.page = page
        self.nombre = nombre
        self.movimientos = movimientos
        self.filtros = filtros
        self.on_filtrar = on_filtrar
        self._on_inicio = on_nav_inicio
        self._on_operar = on_nav_operar
        self._on_historial = on_nav_historial
        self.on_logout = on_logout

        self._filtro_activo = "Todas"
        self._botones_filtro: dict[str, ft.Container] = {}
        self._col_filas = ft.Column(spacing=14)
        self._lbl_cuenta = ft.Text(
            "Todas las cuentas",
            size=12,
            color=theme.VIOLETA_CLARO,
            weight=ft.FontWeight.W_600,
        )

    def build(self) -> ft.Control:
        self._configurar_pagina()

        card = ft.Container(
            padding=18,
            bgcolor=theme.PANEL,
            border_radius=20,
            border=ft.border.all(1.5, theme.BORDE_NEON),
            shadow=ft.BoxShadow(
                blur_radius=12,
                color=theme.BORDE_NEON,
                offset=ft.Offset(0, 0),
            ),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            self._encabezado("FECHA", 2),
                            self._encabezado("OPERACIÓN", 2),
                            self._encabezado("CUENTA", 3),
                            ft.Text(
                                "MONTO",
                                size=11,
                                color=theme.VIOLETA,
                                text_align=ft.TextAlign.RIGHT,
                                expand=3,
                            ),
                        ],
                    ),
                    ft.Divider(height=1, color="#261b3e"),
                    ft.Container(
                        height=250,
                        content=ft.Column(
                            scroll=ft.ScrollMode.ADAPTIVE,
                            controls=[self._col_filas],
                        ),
                    ),
                ],
            ),
        )

        layout = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
            controls=[
                self._header(),
                ft.Column(
                    spacing=14,
                    controls=[
                        ft.Column(
                            spacing=0,
                            controls=[
                                ft.Text(
                                    "HISTORIAL",
                                    size=12,
                                    color=theme.VIOLETA,
                                    weight=ft.FontWeight.W_600,
                                ),
                                ft.Text(
                                    "Movimientos",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=theme.BLANCO,
                                ),
                            ],
                        ),
                        ft.Row(
                            spacing=8,
                            controls=[
                                self._chip_filtro("Todas"),
                                *[
                                    self._chip_filtro(filtro)
                                    for filtro in self.filtros
                                ],
                            ],
                        ),
                        card,
                    ],
                ),
                barra_navegacion(
                    "historial",
                    self._on_inicio,
                    self._on_operar,
                    self._on_historial,
                ),
            ],
        )
        self._render_movimientos(self.movimientos)
        return ft.Container(content=layout, padding=16, expand=True)

    def _configurar_pagina(self) -> None:
        self.page.title = "Capital Bank - Historial"
        self.page.window_width = 520
        self.page.window_height = 700
        self.page.window_resizable = True
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.bgcolor = theme.FONDO

    @staticmethod
    def _encabezado(texto: str, expand: int) -> ft.Text:
        return ft.Text(
            texto,
            size=11,
            color=theme.VIOLETA,
            expand=expand,
        )

    def _header(self) -> ft.Row:
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=12,
                    controls=[
                        ft.Container(
                            width=46,
                            height=46,
                            border_radius=14,
                            border=ft.border.all(1.5, theme.VIOLETA),
                            alignment=ft.Alignment(0, 0),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=0,
                                controls=[
                                    ft.Icon(
                                        ft.Icons.ACCOUNT_BALANCE,
                                        size=18,
                                        color=theme.VIOLETA,
                                    ),
                                    ft.Text(
                                        "C|B",
                                        color=theme.VIOLETA,
                                        weight=ft.FontWeight.BOLD,
                                        size=9,
                                    ),
                                ],
                            ),
                        ),
                        ft.Column(
                            spacing=2,
                            controls=[
                                self._lbl_cuenta,
                                ft.Text(
                                    f"Hola, {self.nombre}",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=theme.BLANCO,
                                ),
                            ],
                        ),
                    ],
                ),
                ft.Container(
                    padding=ft.Padding(12, 6, 12, 6),
                    border=ft.border.all(1, theme.BORDE_NEON),
                    border_radius=20,
                    on_click=lambda _e: self.on_logout(),
                    content=ft.Row(
                        spacing=6,
                        controls=[
                            ft.Icon(
                                ft.Icons.LOGOUT,
                                size=14,
                                color=theme.VIOLETA,
                            ),
                            ft.Text(
                                "Cerrar sesión",
                                size=11,
                                color=theme.VIOLETA,
                            ),
                        ],
                    ),
                ),
            ],
        )

    def _chip_filtro(self, texto: str) -> ft.Container:
        activo = texto == self._filtro_activo
        boton = ft.Container(
            expand=True,
            padding=ft.Padding(0, 8, 0, 8),
            bgcolor=theme.BOTON_NEON if activo else None,
            border=None if activo else ft.border.all(1, theme.BORDE_NEON),
            border_radius=20,
            alignment=ft.Alignment(0, 0),
            on_click=lambda _e, t=texto: self._aplicar_filtro(t),
            content=ft.Text(
                texto,
                color=theme.BLANCO,
                size=12,
                weight=ft.FontWeight.W_500,
            ),
        )
        self._botones_filtro[texto] = boton
        return boton

    def _aplicar_filtro(self, texto: str) -> None:
        self._filtro_activo = texto
        self._lbl_cuenta.value = (
            "Todas las cuentas" if texto == "Todas" else texto
        )
        for etiqueta, boton in self._botones_filtro.items():
            activo = etiqueta == texto
            boton.bgcolor = theme.BOTON_NEON if activo else None
            boton.border = None if activo else ft.border.all(1, theme.BORDE_NEON)
        self.page.update()
        self.on_filtrar(texto)

    def actualizar_movimientos(self, movimientos: list[MovimientoVista]) -> None:
        self._render_movimientos(movimientos)
        self.page.update()

    def _render_movimientos(self, movimientos: list[MovimientoVista]) -> None:
        self._col_filas.controls.clear()

        if not movimientos:
            self._col_filas.controls.append(
                ft.Container(
                    padding=20,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text(
                        "Sin movimientos registrados",
                        color=theme.TEXTO_SUAVE,
                        size=13,
                    ),
                )
            )
        else:
            for movimiento in movimientos:
                self._col_filas.controls.append(
                    self._fila(movimiento)
                )

    @staticmethod
    def _fila(movimiento: MovimientoVista) -> ft.Row:
        color = (
            theme.VERDE_NEON if movimiento.monto > 0 else theme.ROJO_NEON
        )
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(movimiento.fecha, size=12, color=theme.BLANCO, expand=2),
                ft.Text(movimiento.operacion, size=12, color=theme.BLANCO, expand=2),
                ft.Text(movimiento.cuenta, size=12, color=theme.BLANCO, expand=3),
                ft.Text(
                    formatear_monto_movimiento(movimiento.monto),
                    size=12,
                    weight=ft.FontWeight.W_500,
                    color=color,
                    text_align=ft.TextAlign.RIGHT,
                    expand=3,
                ),
            ],
        )
