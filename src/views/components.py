"""Componentes visuales reutilizables (solo Flet, sin lógica de negocio)."""

import flet as ft

from src.views import theme


def campo(
    label: str,
    value: str = "",
    password: bool = False,
    hint_text: str | None = None,
    expand: bool = False,
    width: int | None = None,
) -> ft.TextField:
    return ft.TextField(
        label=label,
        value=value,
        password=password,
        can_reveal_password=password,
        hint_text=hint_text,
        width=width,
        expand=expand,
        label_style=ft.TextStyle(color=theme.VIOLETA_CLARO, size=13),
        hint_style=ft.TextStyle(color=theme.TEXTO_OSCURO, size=13),
        text_style=ft.TextStyle(color=theme.BLANCO, size=14),
        bgcolor=theme.PANEL_SECUNDARIO,
        border_color=theme.VIOLETA_OSCURO,
        focused_border_color=theme.VIOLETA_CLARO,
        border_width=1.3,
        focused_border_width=1.8,
        border_radius=8,
        cursor_color=theme.VIOLETA_CLARO,
        content_padding=ft.Padding(16, 12, 16, 12),
    )


def boton_primario(texto: str, on_click, width: int | None = None) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        content=ft.Text(texto, size=15, weight=ft.FontWeight.BOLD),
        on_click=on_click,
        height=48,
        width=width,
        expand=width is None,
        bgcolor=theme.VIOLETA,
        color=theme.BLANCO,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            overlay_color="#25FFFFFF",
        ),
    )


def boton_secundario(
    texto: str, on_click, width: int | None = None
) -> ft.OutlinedButton:
    return ft.OutlinedButton(
        content=ft.Text(
            texto,
            size=14,
            weight=ft.FontWeight.BOLD,
            color=theme.VIOLETA_CLARO,
        ),
        on_click=on_click,
        height=48,
        width=width,
        expand=width is None,
        style=ft.ButtonStyle(
            side=ft.BorderSide(width=1.4, color=theme.VIOLETA),
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )


def etiqueta(texto: str) -> ft.Text:
    return ft.Text(
        texto,
        size=13,
        weight=ft.FontWeight.W_500,
        color=theme.VIOLETA_CLARO,
    )


def texto_secundario(texto: str, size: int = 13) -> ft.Text:
    return ft.Text(texto, size=size, color=theme.TEXTO_SUAVE)


def divisor() -> ft.Divider:
    return ft.Divider(height=1, thickness=1, color=theme.LINEA)


def _nav_btn(icono, texto: str, activo: bool, on_click) -> ft.Container:
    color = theme.BLANCO if activo else theme.TEXTO_SUAVE
    return ft.Container(
        expand=True,
        padding=ft.Padding(0, 8, 0, 8),
        bgcolor=theme.BOTON_NEON if activo else None,
        border_radius=25,
        on_click=on_click,
        content=ft.Column(
            spacing=2,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(icono, color=color, size=20),
                ft.Text(texto, size=10, color=color),
            ],
        ),
    )


def barra_navegacion(
    activo: str,
    on_inicio,
    on_operar,
    on_historial,
) -> ft.Container:
    """Barra inferior Inicio / Operar / Historial, sin imports de controladores."""
    return ft.Container(
        padding=4,
        border=ft.border.all(1.5, theme.BORDE_NEON),
        border_radius=30,
        content=ft.Row(
            controls=[
                _nav_btn(ft.Icons.HOME_OUTLINED, "Inicio", activo == "inicio", on_inicio),
                _nav_btn(ft.Icons.SWAP_HORIZ, "Operar", activo == "operar", on_operar),
                _nav_btn(ft.Icons.SCHEDULE, "Historial", activo == "historial", on_historial),
            ],
        ),
    )


def mostrar_snack(page: ft.Page, texto: str, error: bool = False) -> None:
    """Aviso efímero: es presentación pura."""
    page.snack_bar = ft.SnackBar(
        ft.Text(texto, color=theme.BLANCO),
        bgcolor=theme.ROJO if error else theme.VERDE,
    )
    page.snack_bar.open = True
    page.update()
