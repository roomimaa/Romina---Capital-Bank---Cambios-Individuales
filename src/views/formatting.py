"""Formato de datos para mostrar. Es lógica de presentación, no de negocio."""


def formatear_monto(monto: float) -> str:
    """12500.0 -> '$ 12.500,00'."""
    valor = f"{abs(monto):,.2f}"
    return "$ " + valor.replace(".", "X").replace(",", ".").replace("X", ",")


def formatear_monto_movimiento(monto: float) -> str:
    """Monto con signo: '+ 12.500,00' / '- 1.000,00'."""
    signo = "+ " if monto > 0 else "- "
    valor = f"{abs(monto):,.2f}"
    return signo + valor.replace(".", "X").replace(",", ".").replace("X", ",")


def formatear_fecha(fecha) -> str:
    if hasattr(fecha, "strftime"):
        return fecha.strftime("%d/%m/%Y")
    return str(fecha)[:10]


def etiqueta_operacion(tipo: str) -> str:
    return {"deposito": "Depositar", "retiro": "Retirar"}.get(
        tipo, str(tipo).capitalize()
    )
