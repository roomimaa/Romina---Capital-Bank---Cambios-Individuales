"""Vista de operaciones (depósito / retiro). Solo interfaz."""

import flet as ft

from src.views import theme
from src.views.components import barra_navegacion, mostrar_snack
from src.views.view_models import CuentaVista


class OperationsView:
    def __init__(
        self,
        page: ft.Page,
        nombre: str,
        cuentas: list[CuentaVista],
        on_ejecutar,
        on_nav_inicio,
        on_nav_operar,
        on_nav_historial,
    ):
        self.page = page
        self.nombre = nombre
        self.cuentas = cuentas
        self.on_ejecutar = on_ejecutar
        self._on_inicio = on_nav_inicio
        self._on_operar = on_nav_operar
        self._on_historial = on_nav_historial

        self._cuenta_id = cuentas[0].id_cuenta if cuentas else None
        self._tipo_operacion = "deposito"
        self._botones_cuenta: dict[int, ft.Container] = {}

        self._lbl_cuenta = ft.Text(
            cuentas[0].tipo if cuentas else "Sin cuentas",
            size=12,
            color=theme.VIOLETA_CLARO,
            weight=ft.FontWeight.W_600,
        )
        self._lbl_ejecutar = ft.Text(
            "Depositar",
            color=theme.BLANCO,
            size=16,
            weight=ft.FontWeight.BOLD,
        )
        self._monto = ft.TextField(
            value="",
            hint_text="0,00",
            prefix=ft.Text(
                "$  ",
                color=theme.BLANCO,
                size=18,
                weight=ft.FontWeight.BOLD,
            ),
            border_color=theme.BORDE_NEON,
            focused_border_color=theme.VIOLETA,
            border_radius=12,
            text_size=18,
            color=theme.BLANCO,
            height=50,
            keyboard_type=ft.KeyboardType.NUMBER,
        )

    def build(self) -> ft.Control:
        self._configurar_pagina()

        fila_cuentas = ft.Row(
            spacing=10,
            wrap=True,
            controls=[
                self._chip_cuenta(cuenta) for cuenta in self.cuentas
            ]
            or [
                ft.Text(
                    "No tenés cuentas cargadas.",
                    size=13,
                    color=theme.TEXTO_SUAVE,
                )
            ],
        )

        card = ft.Container(
            padding=20,
            bgcolor=theme.PANEL,
            border_radius=20,
            border=ft.border.all(1.5, theme.BORDE_NEON),
            shadow=ft.BoxShadow(
                blur_radius=15,
                color=theme.BORDE_NEON,
                offset=ft.Offset(0, 0),
            ),
            content=ft.Column(
                spacing=16,
                controls=[
                    ft.Column(
                        spacing=2,
                        controls=[
                            self._lbl_cuenta,
                            ft.Text(
                                f"Hola, {self.nombre}",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color=theme.BLANCO,
                            ),
                            ft.Text(
                                "OPERAR",
                                size=14,
                                color=theme.BLANCO,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Depositar o retirar",
                                size=13,
                                color=theme.VIOLETA_CLARO,
                            ),
                        ],
                    ),
                    fila_cuentas,
                    ft.Row(
                        spacing=10,
                        controls=[
                            self._chip_operacion(
                                "Depositar",
                                "deposito",
                                ft.Icons.ARROW_DOWNWARD_ROUNDED,
                            ),
                            self._chip_operacion(
                                "Retirar",
                                "retiro",
                                ft.Icons.ARROW_UPWARD_ROUNDED,
                            ),
                        ],
                    ),
                    self._monto,
                    ft.Container(
                        padding=ft.Padding(0, 12, 0, 12),
                        bgcolor=theme.BOTON_NEON,
                        border_radius=25,
                        alignment=ft.Alignment(0, 0),
                        on_click=self._ejecutar,
                        content=self._lbl_ejecutar,
                    ),
                ],
            ),
        )

        layout = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
            controls=[
                ft.Container(),
                card,
                barra_navegacion(
                    "operar",
                    self._on_inicio,
                    self._on_operar,
                    self._on_historial,
                ),
            ],
        )
        return ft.Container(content=layout, padding=16, expand=True)

    def _configurar_pagina(self) -> None:
        self.page.title = "Capital Bank - Operaciones"
        self.page.window_width = 520
        self.page.window_height = 700
        self.page.window_resizable = True
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.bgcolor = theme.FONDO

    def _chip_cuenta(self, cuenta: CuentaVista) -> ft.Container:
        seleccionada = cuenta.id_cuenta == self._cuenta_id
        boton = ft.Container(
            expand=True,
            padding=ft.Padding(0, 10, 0, 10),
            bgcolor=theme.BOTON_NEON if seleccionada else None,
            border=None
            if seleccionada
            else ft.border.all(1, theme.BORDE_NEON),
            border_radius=20,
            alignment=ft.Alignment(0, 0),
            on_click=lambda _e, c=cuenta: self._seleccionar_cuenta(c),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Icon(
                        ft.Icons.ACCOUNT_BALANCE,
                        color=theme.BLANCO,
                        size=18,
                    ),
                    ft.Text(
                        cuenta.tipo,
                        color=theme.BLANCO,
                        size=13,
                        weight=ft.FontWeight.W_500,
                    ),
                ],
            ),
        )
        self._botones_cuenta[cuenta.id_cuenta] = boton
        return boton

    def _chip_operacion(
        self,
        texto: str,
        tipo: str,
        icono,
    ) -> ft.Container:
        seleccionada = tipo == self._tipo_operacion
        boton = ft.Container(
            expand=True,
            padding=ft.Padding(0, 10, 0, 10),
            bgcolor=theme.BOTON_NEON if seleccionada else None,
            border=None
            if seleccionada
            else ft.border.all(1, theme.BORDE_NEON),
            border_radius=20,
            alignment=ft.Alignment(0, 0),
            on_click=lambda _e: self._seleccionar_operacion(tipo, texto),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Icon(icono, color=theme.BLANCO, size=18),
                    ft.Text(texto, color=theme.BLANCO, size=13),
                ],
            ),
        )
        if tipo == "deposito":
            self._btn_deposito = boton
        else:
            self._btn_retiro = boton
        return boton

    def _seleccionar_cuenta(self, cuenta: CuentaVista) -> None:
        self._cuenta_id = cuenta.id_cuenta
        self._lbl_cuenta.value = cuenta.tipo
        for id_cuenta, boton in self._botones_cuenta.items():
            activo = id_cuenta == cuenta.id_cuenta
            boton.bgcolor = theme.BOTON_NEON if activo else None
            boton.border = None if activo else ft.border.all(1, theme.BORDE_NEON)
        self.page.update()

    def _seleccionar_operacion(self, tipo: str, texto: str) -> None:
        self._tipo_operacion = tipo
        self._lbl_ejecutar.value = texto
        for boton, boton_tipo in (
            (self._btn_deposito, "deposito"),
            (self._btn_retiro, "retiro"),
        ):
            activo = boton_tipo == tipo
            boton.bgcolor = theme.BOTON_NEON if activo else None
            boton.border = None if activo else ft.border.all(1, theme.BORDE_NEON)
        self.page.update()

    def _ejecutar(self, _evento) -> None:
        if self._cuenta_id is None:
            self.mostrar_mensaje("No tenés cuentas cargadas.", error=True)
            return
        self.on_ejecutar(
            self._cuenta_id,
            self._tipo_operacion,
            self._monto.value or "",
        )

    def limpiar_monto(self) -> None:
        self._monto.value = ""
        self.page.update()

    def mostrar_mensaje(self, texto: str, error: bool = False) -> None:
        mostrar_snack(self.page, texto, error)
