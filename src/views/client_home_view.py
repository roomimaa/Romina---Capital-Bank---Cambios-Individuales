"""Vista del home del cliente. No consulta la base ni calcula reglas."""

import flet as ft

from src.views import theme
from src.views.components import barra_navegacion, mostrar_snack
from src.views.formatting import formatear_monto
from src.views.view_models import CuentaVista


class ClientHomeView:
    def __init__(
        self,
        page: ft.Page,
        nombre: str,
        cuentas: list[CuentaVista],
        total: float,
        on_logout,
        on_inicio,
        on_operar,
        on_historial,
    ):
        self.page = page
        self.nombre = nombre
        self.cuentas = cuentas
        self.total = total
        self.on_logout = on_logout
        self._on_inicio = on_inicio
        self._on_operar = on_operar
        self._on_historial = on_historial

        self._oculto_total = True
        self._ocultos = [False] * len(cuentas)
        self._tarjetas: list[dict] = []

        self._lbl_total = ft.Text(
            self._texto_saldo(self.total, False),
            size=20,
            weight=ft.FontWeight.BOLD,
            color=theme.BLANCO,
        )
        self._btn_ojo_total = ft.IconButton(
            icon=ft.Icons.VISIBILITY_OFF,
            icon_color=theme.VIOLETA_CLARO,
            icon_size=18,
            bgcolor=theme.LINEA,
            style=ft.ButtonStyle(shape=ft.CircleBorder()),
            tooltip="Mostrar/ocultar saldos",
            on_click=lambda _e: self._alternar_total(),
        )

    def build(self) -> ft.Control:
        self._configurar_pagina()

        contenido = (
            ft.Column(
                spacing=16,
                controls=[
                    self._construir_tarjeta(cuenta, indice)
                    for indice, cuenta in enumerate(self.cuentas)
                ],
            )
            if self.cuentas
            else ft.Text(
                "No tenés cuentas cargadas.",
                size=13,
                color=theme.TEXTO_OSCURO,
                text_align=ft.TextAlign.CENTER,
            )
        )

        layout = ft.Column(
            expand=True,
            spacing=18,
            controls=[
                self._header(),
                self._control_total(),
                ft.Column(
                    scroll=ft.ScrollMode.ADAPTIVE,
                    spacing=16,
                    controls=[contenido],
                ),
                barra_navegacion(
                    "inicio",
                    self._on_inicio,
                    self._on_operar,
                    self._on_historial,
                ),
            ],
        )
        return ft.Container(content=layout, padding=24, expand=True)

    def _configurar_pagina(self) -> None:
        self.page.title = "Capital Bank - Home Cliente"
        self.page.window_width = 420
        self.page.window_height = 680
        self.page.window_resizable = False
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.bgcolor = theme.FONDO

    def _header(self) -> ft.Row:
        return ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Column(
                    spacing=3,
                    controls=[
                        ft.Text(
                            f"Hola, {self.nombre} 👋",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=theme.BLANCO,
                        ),
                        ft.Text(
                            "Estas son tus cuentas en Capital Bank",
                            size=13,
                            color=theme.TEXTO_SUAVE,
                        ),
                    ],
                ),
                ft.OutlinedButton(
                    content=ft.Text(
                        "Cerrar sesión",
                        size=12,
                        color=theme.VIOLETA_CLARO,
                    ),
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(width=1, color=theme.VIOLETA),
                        shape=ft.RoundedRectangleBorder(radius=18),
                        padding=ft.Padding(14, 6, 14, 6),
                    ),
                    on_click=lambda _e: self.on_logout(),
                ),
            ],
        )

    def _control_total(self) -> ft.Container:
        return ft.Container(
            padding=ft.Padding(18, 14, 18, 14),
            bgcolor="#181820",
            border_radius=15,
            border=ft.border.all(1, theme.LINEA),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "Total en tus cuentas",
                        size=14,
                        color=theme.TEXTO_SUAVE,
                    ),
                    ft.Row(
                        spacing=6,
                        controls=[self._lbl_total, self._btn_ojo_total],
                    ),
                ],
            ),
        )

    def _construir_tarjeta(self, cuenta: CuentaVista, indice: int) -> ft.Container:
        lbl_saldo = ft.Text(
            self._texto_saldo(cuenta.saldo, False),
            size=26,
            weight=ft.FontWeight.BOLD,
            color=theme.BLANCO,
        )
        btn_ojo = ft.IconButton(
            icon=ft.Icons.VISIBILITY_OFF,
            icon_color=theme.VIOLETA_CLARO,
            icon_size=16,
            bgcolor=theme.LINEA,
            style=ft.ButtonStyle(shape=ft.CircleBorder()),
            tooltip="Mostrar/ocultar saldo",
            on_click=lambda _e, i=indice: self._alternar_individual(i),
        )
        self._tarjetas.append({"lbl_saldo": lbl_saldo, "btn_ojo": btn_ojo})

        return ft.Container(
            padding=20,
            bgcolor="#181820",
            border_radius=15,
            border=ft.border.all(1, theme.LINEA),
            shadow=ft.BoxShadow(
                blur_radius=15,
                color=theme.BORDE_NEON,
                offset=ft.Offset(0, 0),
            ),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(
                                        f"{cuenta.tipo} · tipo {indice + 1}",
                                        size=13,
                                        weight=ft.FontWeight.BOLD,
                                        color=theme.TEXTO_SUAVE,
                                    ),
                                    ft.Text(
                                        f"Nro. {cuenta.numero}",
                                        size=11,
                                        color=theme.TEXTO_OSCURO,
                                    ),
                                ],
                            ),
                            ft.Container(
                                content=ft.Text(
                                    "activa",
                                    size=10,
                                    weight=ft.FontWeight.BOLD,
                                    color=theme.VIOLETA_CLARO,
                                ),
                                padding=ft.Padding(10, 3, 10, 3),
                                bgcolor=theme.LINEA,
                                border_radius=12,
                            ),
                        ],
                    ),
                    ft.Container(height=6),
                    lbl_saldo,
                    ft.Text(
                        "SALDO DISPONIBLE",
                        size=10,
                        color=theme.TEXTO_OSCURO,
                    ),
                    ft.Row(
                        controls=[btn_ojo],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                ],
            ),
        )

    @staticmethod
    def _texto_saldo(monto: float, visible: bool) -> str:
        return formatear_monto(monto) if visible else "••••••"

    def _alternar_total(self) -> None:
        self._oculto_total = not self._oculto_total
        self._refrescar_saldos()

    def _alternar_individual(self, indice: int) -> None:
        self._ocultos[indice] = not self._ocultos[indice]
        self._refrescar_saldos()

    def _refrescar_saldos(self) -> None:
        self._lbl_total.value = self._texto_saldo(
            self.total, not self._oculto_total
        )
        self._btn_ojo_total.icon = (
            ft.Icons.VISIBILITY_OFF
            if self._oculto_total
            else ft.Icons.VISIBILITY
        )
        for indice, tarjeta in enumerate(self._tarjetas):
            visible = not self._oculto_total and not self._ocultos[indice]
            tarjeta["lbl_saldo"].value = self._texto_saldo(
                self.cuentas[indice].saldo, visible
            )
            tarjeta["btn_ojo"].icon = (
                ft.Icons.VISIBILITY if visible else ft.Icons.VISIBILITY_OFF
            )
        self.page.update()

    def mostrar_mensaje(self, texto: str, error: bool = False) -> None:
        mostrar_snack(self.page, texto, error)
