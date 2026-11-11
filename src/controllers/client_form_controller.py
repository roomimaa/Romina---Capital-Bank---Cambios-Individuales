"""Controlador de alta/edición de clientes y sus cuentas."""

from src.controllers.base_controller import BaseController
from src.views.client_form_view import ClientFormView
from src.views.view_models import ClienteFormVista, CuentaVista


class ClientFormController(BaseController):
    requiere_personal = True

    def __init__(self, contexto, dni: str | None = None):
        super().__init__(contexto)
        self._dni = dni
        self._cliente = None
        self.view = None

    def construir(self):
        if self._dni:
            self._cliente = self.ctx.clientes.obtener_cliente(self._dni)
            if self._cliente is None:
                self.ir(
                    "home_personal",
                    mensaje="No existe un cliente con ese DNI.",
                    error=True,
                )
                return None

        self.view = ClientFormView(
            self.page,
            cliente=self._cliente_vista(),
            cuentas=self._cuentas_vista(),
            on_guardar=self._guardar,
            on_agregar_cuenta=self._agregar_cuenta,
            on_volver=lambda: self.ir("home_personal"),
        )
        return self.view.build()

    # ------------------------------------------------------------------
    # Eventos de la vista
    # ------------------------------------------------------------------

    def _guardar(self, datos: dict) -> None:
        try:
            if datos["dni_actual"] is None:
                self.ctx.clientes.crear_cliente(
                    datos["nombre"],
                    datos["apellido"],
                    datos["dni"],
                    clave=datos["clave"] or None,
                )
                mensaje = "Cliente creado correctamente."
            else:
                self.ctx.clientes.actualizar_cliente(
                    datos["dni_actual"],
                    datos["nombre"],
                    datos["apellido"],
                    datos["dni"],
                    clave=datos["clave"] or None,
                )
                mensaje = "Cliente actualizado correctamente."
        except ValueError as error:
            self.view.mostrar_mensaje(str(error), error=True)
            return
        except Exception:
            self.view.mostrar_mensaje(
                "No se pudo guardar el cliente. Intentá nuevamente.",
                error=True,
            )
            return

        self._dni = (datos["dni"] or "").strip()
        self._cliente = self.ctx.clientes.obtener_cliente(self._dni)
        if self._cliente is not None:
            self.view.set_cliente(self._cliente_vista())
        self.view.set_cuentas(self._cuentas_vista())
        self.view.mostrar_mensaje(mensaje)

    def _agregar_cuenta(self, datos: dict) -> None:
        if datos["dni"] is None:
            self.view.mostrar_mensaje(
                "Guardá el cliente antes de agregar cuentas.", error=True
            )
            return

        try:
            self.ctx.clientes.agregar_cuenta(
                datos["dni"],
                datos["numero"],
                datos["tipo"],
                datos["saldo"],
            )
        except ValueError as error:
            self.view.mostrar_mensaje(str(error), error=True)
            return
        except Exception:
            self.view.mostrar_mensaje(
                "No se pudo agregar la cuenta. Intentá nuevamente.",
                error=True,
            )
            return

        self.view.limpiar_formulario_cuenta()
        self.view.set_cuentas(self._cuentas_vista())
        self.view.mostrar_mensaje("Cuenta agregada correctamente.")

    # ------------------------------------------------------------------
    # Mapeo dominio -> datos de vista
    # ------------------------------------------------------------------

    def _cliente_vista(self) -> ClienteFormVista | None:
        if self._cliente is None:
            return None
        return ClienteFormVista(
            nombre=self._cliente.nombre,
            apellido=self._cliente.apellido,
            dni=self._cliente.dni,
        )

    def _cuentas_vista(self) -> list[CuentaVista]:
        if self._cliente is None:
            return []
        return [
            CuentaVista(
                id_cuenta=cuenta.id_cuenta,
                numero=cuenta.numero,
                tipo=cuenta.tipo,
                saldo=cuenta.saldo,
            )
            for cuenta in self._cliente.cuentas
        ]
