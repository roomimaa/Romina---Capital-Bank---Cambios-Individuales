"""Vista de alta/edición de cliente y sus cuentas. Solo interfaz."""

import flet as ft

from src.views import theme
from src.views.components import (
    boton_primario,
    boton_secundario,
    campo,
    divisor,
    mostrar_snack,
    texto_secundario,
)
from src.views.formatting import formatear_monto
from src.views.view_models import ClienteFormVista, CuentaVista


class ClientFormView:
    def __init__(
        self,
        page: ft.Page,
        cliente: ClienteFormVista | None,
        cuentas: list[CuentaVista],
        on_guardar,
        on_agregar_cuenta,
        on_volver,
    ):
        self.page = page
        self.cliente = cliente
        self.cuentas = cuentas
        self.on_guardar = on_guardar
        self.on_agregar_cuenta = on_agregar_cuenta
        self.on_volver = on_volver

        self._dni_actual = cliente.dni if cliente else None

        self._titulo = ft.Text(
            "Alta de Cliente" if cliente is None else "Editar Cliente",
            size=34,
            weight=ft.FontWeight.BOLD,
            color=theme.BLANCO,
        )
        self._subtitulo = ft.Text(
            "Paso a paso para registrar un nuevo usuario."
            if cliente is None
            else f"Modificá los datos de {cliente.nombre} {cliente.apellido}.",
            size=15,
            color=theme.VIOLETA_CLARO,
        )

        self._txt_nombre = campo(
            "Nombre",
            value=cliente.nombre if cliente else "",
            hint_text="ej. Alejandro",
            expand=True,
        )
        self._txt_apellido = campo(
            "Apellido",
            value=cliente.apellido if cliente else "",
            hint_text="ej. Morales",
            expand=True,
        )
        self._txt_dni = campo(
            "DNI",
            value=cliente.dni if cliente else "",
            hint_text="Sin puntos, ej. 42345678",
            expand=True,
        )
        self._txt_clave = campo(
            "Clave nueva (vacío = no cambia)"
            if cliente is not None
            else "Clave",
            password=True,
            hint_text="••••••••",
            expand=True,
        )

        self._col_cuentas = ft.Column(spacing=10)
        self._txt_nro = campo(
            "Número de cuenta",
            hint_text="ej. 100001",
            expand=True,
        )
        self._txt_saldo = campo(
            "Saldo inicial",
            hint_text="$ 0,00",
            expand=True,
        )
        self._dd_tipo = ft.Dropdown(
            label="Tipo de cuenta",
            expand=True,
            options=[
                ft.dropdown.Option("Ahorro"),
                ft.dropdown.Option("Corriente"),
            ],
            label_style=ft.TextStyle(color=theme.VIOLETA_CLARO, size=13),
            text_style=ft.TextStyle(color=theme.BLANCO, size=14),
            bgcolor=theme.PANEL_SECUNDARIO,
            border_color=theme.VIOLETA_OSCURO,
            focused_border_color=theme.VIOLETA_CLARO,
            border_width=1.3,
            focused_border_width=1.8,
            border_radius=8,
            color=theme.BLANCO,
            content_padding=ft.Padding(16, 12, 16, 12),
        )

    def build(self) -> ft.Control:
        self._configurar_pagina()
        self._render_cuentas()

        panel = ft.Container(
            width=850,
            padding=ft.Padding(34, 28, 34, 28),
            bgcolor=theme.PANEL,
            border_radius=16,
            border=ft.border.all(2, theme.VIOLETA),
            shadow=ft.BoxShadow(
                blur_radius=24,
                spread_radius=1,
                color="#70A020F0",
                offset=ft.Offset(0, 4),
            ),
            content=ft.Column(
                spacing=18,
                controls=[
                    self._titulo,
                    self._subtitulo,
                    ft.Container(height=2),
                    ft.Row(spacing=18, controls=[self._txt_nombre, self._txt_apellido]),
                    ft.Row(spacing=18, controls=[self._txt_dni, self._txt_clave]),
                    ft.Row(
                        controls=[
                            ft.Container(expand=True),
                            ft.Text(
                                "Mínimo 4 caracteres",
                                size=11,
                                color=theme.TEXTO_SUAVE,
                            ),
                        ],
                    ),
                    divisor(),
                    ft.Text(
                        "Cuentas del cliente",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=theme.VIOLETA_CLARO,
                    ),
                    self._col_cuentas,
                    ft.Row(
                        spacing=14,
                        controls=[self._txt_nro, self._dd_tipo, self._txt_saldo],
                    ),
                    ft.ElevatedButton(
                        content=ft.Text(
                            "AGREGAR CUENTA",
                            weight=ft.FontWeight.BOLD,
                        ),
                        on_click=self._click_agregar,
                        bgcolor="#23142E",
                        color=theme.VIOLETA_CLARO,
                        height=44,
                        width=220,
                        style=ft.ButtonStyle(
                            side=ft.BorderSide(1.2, theme.VIOLETA),
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                    ),
                    divisor(),
                    ft.Row(
                        spacing=20,
                        controls=[
                            boton_secundario(
                                "Cancelar",
                                lambda _e: self.on_volver(),
                            ),
                            boton_primario(
                                "Guardar cliente",
                                self._click_guardar,
                            ),
                        ],
                    ),
                ],
            ),
        )

        return ft.Container(
            width=float("inf"),
            padding=ft.Padding(40, 26, 40, 40),
            alignment=ft.Alignment(0, -1),
            content=ft.Column(
                width=850,
                spacing=18,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                controls=[self._logo(), panel],
            ),
        )

    def _configurar_pagina(self) -> None:
        self.page.title = "Capital Bank - Gestión cliente"
        self.page.bgcolor = theme.FONDO
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.padding = 0

    @staticmethod
    def _logo() -> ft.Row:
        return ft.Row(
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=54,
                    height=54,
                    border_radius=14,
                    border=ft.border.all(2, theme.VIOLETA),
                    bgcolor="#15101D",
                    alignment=ft.Alignment(0, 0),
                    shadow=ft.BoxShadow(
                        blur_radius=18,
                        color="#90A020F0",
                    ),
                    content=ft.Icon(
                        ft.Icons.ACCOUNT_BALANCE,
                        color=theme.VIOLETA_CLARO,
                        size=30,
                    ),
                ),
                ft.Text(
                    "CAPITAL\nBANK",
                    size=17,
                    weight=ft.FontWeight.BOLD,
                    color=theme.BLANCO,
                ),
                ft.Container(
                    width=1,
                    height=22,
                    bgcolor=theme.LINEA,
                    margin=ft.Margin(6, 0, 6, 0),
                ),
                ft.Text(
                    "VISTA PERSONAL",
                    size=13,
                    weight=ft.FontWeight.W_500,
                    color=theme.VIOLETA_CLARO,
                ),
            ],
        )

    def _render_cuentas(self) -> None:
        self._col_cuentas.controls.clear()

        if self._dni_actual is None:
            self._col_cuentas.controls.append(
                texto_secundario("Guardá el cliente para poder agregar cuentas.")
            )
            return

        if not self.cuentas:
            self._col_cuentas.controls.append(
                texto_secundario(
                    "Este cliente todavía no tiene cuentas registradas."
                )
            )
            return

        for cuenta in self.cuentas:
            self._col_cuentas.controls.append(
                ft.Container(
                    padding=ft.Padding(14, 11, 14, 11),
                    bgcolor=theme.PANEL_CLARO,
                    border_radius=8,
                    border=ft.border.all(1, "#3B2250"),
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                width=24,
                                height=24,
                                border_radius=6,
                                bgcolor=theme.VIOLETA,
                                alignment=ft.Alignment(0, 0),
                                content=ft.Icon(
                                    ft.Icons.CHECK,
                                    color=theme.BLANCO,
                                    size=16,
                                ),
                            ),
                            ft.Text(
                                cuenta.numero,
                                color=theme.BLANCO,
                                size=14,
                                weight=ft.FontWeight.W_500,
                                expand=True,
                            ),
                            ft.Text(
                                formatear_monto(cuenta.saldo),
                                color=theme.VIOLETA_CLARO,
                                size=14,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                )
            )

    def _click_guardar(self, _evento) -> None:
        self.on_guardar(
            {
                "dni_actual": self._dni_actual,
                "nombre": self._txt_nombre.value or "",
                "apellido": self._txt_apellido.value or "",
                "dni": self._txt_dni.value or "",
                "clave": self._txt_clave.value or "",
            }
        )

    def _click_agregar(self, _evento) -> None:
        self.on_agregar_cuenta(
            {
                "dni": self._dni_actual,
                "numero": self._txt_nro.value or "",
                "tipo": self._dd_tipo.value,
                "saldo": self._txt_saldo.value or "",
            }
        )

    # ------------------------------------------------------------------
    # Actualizaciones que pide el controlador
    # ------------------------------------------------------------------

    def set_cliente(self, cliente: ClienteFormVista) -> None:
        self.cliente = cliente
        self._dni_actual = cliente.dni
        self._txt_nombre.value = cliente.nombre
        self._txt_apellido.value = cliente.apellido
        self._txt_dni.value = cliente.dni
        self._titulo.value = "Editar Cliente"
        self._subtitulo.value = (
            f"Modificá los datos de {cliente.nombre} {cliente.apellido}."
        )
        self._txt_clave.label = "Clave nueva (vacío = no cambia)"
        self.page.update()

    def set_cuentas(self, cuentas: list[CuentaVista]) -> None:
        self.cuentas = cuentas
        self._render_cuentas()
        self.page.update()

    def limpiar_formulario_cuenta(self) -> None:
        self._txt_nro.value = ""
        self._txt_saldo.value = ""
        self._dd_tipo.value = None
        self.page.update()

    def mostrar_mensaje(self, texto: str, error: bool = False) -> None:
        mostrar_snack(self.page, texto, error)
