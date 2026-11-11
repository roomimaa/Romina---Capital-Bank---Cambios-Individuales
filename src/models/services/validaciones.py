"""Validaciones y normalizaciones compartidas por los servicios.

No contienen Flet ni SQL: son funciones puras y fáciles de testear.
"""

TIPOS_CUENTA = {"ahorro": "Ahorro", "corriente": "Corriente"}


def texto_obligatorio(valor, nombre_campo: str) -> str:
    limpio = (valor or "").strip()
    if not limpio:
        raise ValueError(f"El campo {nombre_campo} es obligatorio.")
    return limpio


def _parsear_numero(texto) -> float:
    limpio = str(texto or "").strip().replace("$", "").replace(" ", "")
    if not limpio:
        raise ValueError("Ingresá un monto.")
    # Acepta formato argentino (1.000,50) y formato con punto decimal (1000.50).
    if "," in limpio:
        limpio = limpio.replace(".", "").replace(",", ".")
    try:
        return float(limpio)
    except (TypeError, ValueError) as error:
        raise ValueError("El monto debe ser un número.") from error


def parsear_monto(texto) -> float:
    """Convierte el texto del usuario en un monto positivo."""
    monto = _parsear_numero(texto)
    if monto <= 0:
        raise ValueError("El monto debe ser mayor a cero.")
    return monto


def parsear_saldo_inicial(texto) -> float:
    """Convierte el texto del usuario en un saldo mayor o igual a cero."""
    if texto is None or str(texto).strip() == "":
        return 0.0
    saldo = _parsear_numero(texto)
    if saldo < 0:
        raise ValueError("El saldo no puede ser negativo.")
    return saldo


def normalizar_tipo_cuenta(tipo) -> str:
    clave = (tipo or "").strip().lower()
    if clave not in TIPOS_CUENTA:
        raise ValueError("El tipo de cuenta debe ser 'Ahorro' o 'Corriente'.")
    return TIPOS_CUENTA[clave]
