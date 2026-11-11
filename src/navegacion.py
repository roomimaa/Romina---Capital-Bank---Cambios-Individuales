"""Utilidades puras de navegación (sin Flet ni base de datos)."""


def nombre_cuenta_para_header(nombre_cuenta=None):
    """Devuelve el nombre visible de la cuenta para el encabezado."""
    nombre = (nombre_cuenta or "").strip()
    if not nombre or nombre.lower() == "todas":
        return "Mercado Pago"
    texto = nombre.lower()
    if any(token in texto for token in ("mercado", "pago", "corriente", "ahorro")):
        return "Mercado Pago"
    return nombre.title()
