"""Servicio de autenticación.

Decide el rol del usuario y arma su identidad de sesión. No conoce Flet.
"""

from src.models.entities import Cliente, Cuenta
from src.models.repositories import DAO


class AuthService:
    """Autentica por DNI y clave y devuelve la identidad del usuario."""

    def __init__(self, dao: DAO):
        self.dao = dao

    def autenticar(self, dni: str, clave: str) -> dict | None:
        dni = (dni or "").strip()
        clave = (clave or "").strip()
        if not dni or not clave:
            return None

        persona = self.dao.obtener_persona_por_dni(dni)
        if persona is None or not self.dao.validar_login_por_dni(dni, clave):
            return None

        rol_y_cuentas = self._resolver_rol_y_cuentas(dni, persona[0])
        if rol_y_cuentas is None:
            return None

        rol, cuentas = rol_y_cuentas
        return {
            "dni": persona[3],
            "nombre": persona[1],
            "apellido": persona[2],
            "rol": rol,
            "cuentas": cuentas,
        }

    def _resolver_rol_y_cuentas(
        self, dni: str, id_persona: int
    ) -> tuple[str, list[Cuenta]] | None:
        datos_cliente = self.dao.obtener_cliente_detalle(dni)
        if datos_cliente is not None:
            return "cliente", self._obtener_cuentas(datos_cliente)

        if self.dao.es_empleado(id_persona):
            return "personal", []

        return None

    def _obtener_cuentas(self, datos_cliente: dict) -> list[Cuenta]:
        cliente = Cliente(
            datos_cliente["nombre"],
            datos_cliente["apellido"],
            datos_cliente["dni"],
        )
        filas = self.dao.listar_cuentas(datos_cliente["id_cliente"])
        return [Cuenta.from_dict(fila, cliente) for fila in filas]
