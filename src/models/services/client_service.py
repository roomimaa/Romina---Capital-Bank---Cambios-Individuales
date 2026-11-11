"""Servicio de clientes y cuentas (panel del personal).

Concentra las reglas de negocio del alta, edición y cuentas asociadas.
No conoce Flet.
"""

from dataclasses import dataclass, field

from src.models.entities import Cliente
from src.models.repositories import DAO
from src.models.services.validaciones import (
    normalizar_tipo_cuenta,
    parsear_saldo_inicial,
    texto_obligatorio,
)


@dataclass(frozen=True)
class CuentaResumen:
    id_cuenta: int
    numero: str
    tipo: str
    saldo: float


@dataclass(frozen=True)
class ClienteResumen:
    id_cliente: int
    nombre: str
    apellido: str
    dni: str
    categoria: str | None = None
    estado: str = "ACTIVO"
    cuentas: tuple[CuentaResumen, ...] = field(default_factory=tuple)

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"


class ClientService:
    """Reglas de negocio para la gestión de clientes."""

    def __init__(self, dao: DAO):
        self.dao = dao

    # ------------------------------------------------------------------
    # Lectura
    # ------------------------------------------------------------------

    def listar_clientes(self) -> list[ClienteResumen]:
        resultado = []
        for fila in self.dao.listar_clientes():
            cuentas = tuple(
                self._a_resumen(cuenta)
                for cuenta in self.dao.listar_cuentas(fila["id_cliente"])
            )
            resultado.append(
                ClienteResumen(
                    id_cliente=fila["id_cliente"],
                    nombre=fila["nombre"],
                    apellido=fila["apellido"],
                    dni=fila["dni"],
                    categoria=fila["categoria"],
                    estado=fila["estado"],
                    cuentas=cuentas,
                )
            )
        return resultado

    def obtener_cliente(self, dni: str) -> ClienteResumen | None:
        fila = self.dao.obtener_cliente_detalle((dni or "").strip())
        if fila is None:
            return None
        cuentas = tuple(
            self._a_resumen(cuenta)
            for cuenta in self.dao.listar_cuentas(fila["id_cliente"])
        )
        return ClienteResumen(
            id_cliente=fila["id_cliente"],
            nombre=fila["nombre"],
            apellido=fila["apellido"],
            dni=fila["dni"],
            categoria=fila["categoria"],
            estado=fila["estado"],
            cuentas=cuentas,
        )

    def listar_cuentas(self, id_cliente: int) -> list[CuentaResumen]:
        return [
            self._a_resumen(cuenta)
            for cuenta in self.dao.listar_cuentas(id_cliente)
        ]

    # ------------------------------------------------------------------
    # Escritura
    # ------------------------------------------------------------------

    def crear_cliente(
        self,
        nombre: str,
        apellido: str,
        dni: str,
        clave: str | None = None,
    ) -> int:
        nombre = texto_obligatorio(nombre, "nombre")
        apellido = texto_obligatorio(apellido, "apellido")
        dni = texto_obligatorio(dni, "DNI")

        if self.dao.obtener_persona_por_dni(dni) is not None:
            raise ValueError("Ya existe una persona con ese DNI.")

        cliente = Cliente(nombre, apellido, dni, password=clave)
        return self.dao.guardar_cliente(cliente)

    def actualizar_cliente(
        self,
        dni_actual: str,
        nombre: str,
        apellido: str,
        dni_nuevo: str,
        clave: str | None = None,
    ) -> bool:
        dni_actual = texto_obligatorio(dni_actual, "DNI actual")
        nombre = texto_obligatorio(nombre, "nombre")
        apellido = texto_obligatorio(apellido, "apellido")
        dni_nuevo = texto_obligatorio(dni_nuevo, "DNI")

        # La entidad valida nombre/apellido/DNI y hashea la clave si viene.
        cliente = Cliente(nombre, apellido, dni_nuevo, password=clave)

        if dni_nuevo != dni_actual and self.dao.obtener_persona_por_dni(dni_nuevo):
            raise ValueError("Ya existe otra persona con ese DNI.")

        password_hash = cliente.get_password_hash() if clave else None
        actualizado = self.dao.actualizar_persona(
            dni_actual,
            cliente.get_nombre(),
            cliente.get_apellido(),
            cliente.get_dni(),
            password_hash,
        )
        if not actualizado:
            raise ValueError("El cliente ya no existe.")
        return True

    def agregar_cuenta(
        self,
        dni: str,
        numero: str,
        tipo: str,
        saldo_texto: str | None = None,
    ) -> int:
        numero = texto_obligatorio(numero, "número de cuenta")
        tipo_nombre = normalizar_tipo_cuenta(tipo)
        saldo = parsear_saldo_inicial(saldo_texto)

        cliente = self.dao.obtener_cliente_detalle((dni or "").strip())
        if cliente is None:
            raise ValueError("No existe un cliente con ese DNI.")

        id_tipo = self.dao.buscar_tipo_cuenta(tipo_nombre)
        if id_tipo is None:
            id_tipo = self.dao.guardar_tipo_cuenta(tipo_nombre)

        cuentas = self.dao.listar_cuentas(cliente["id_cliente"])
        if any(cuenta["id_tipo_cuenta"] == id_tipo for cuenta in cuentas):
            raise ValueError(
                f"El cliente ya posee una cuenta de tipo {tipo_nombre}."
            )

        if self.dao.obtener_cuenta_por_numero(numero) is not None:
            raise ValueError("Ya existe una cuenta con ese número.")

        return self.dao.guardar_cuenta(
            numero,
            cliente["id_cliente"],
            id_tipo,
            saldo=saldo,
        )

    @staticmethod
    def _a_resumen(cuenta: dict) -> CuentaResumen:
        return CuentaResumen(
            id_cuenta=cuenta["id_cuenta"],
            numero=cuenta["nro_cuenta"],
            tipo=cuenta["tipo"],
            saldo=cuenta["saldo"],
        )
