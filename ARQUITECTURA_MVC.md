# Arquitectura MVC — Sistema Bancario

Refactorización del proyecto aplicando **MVC en capas** y **SOLID**. La regla de oro:
cada capa solo depende de la capa que tiene inmediatamente debajo.

```
Vista (Flet)  ->  Controlador  ->  Modelo (servicios)  ->  Repositorio (DAO)  ->  SQLite
```

## Estructura

```
main.py                          # composición raíz: DAO + App
src/
├── controllers/                 # CAPA CONTROLADOR (mediadores)
│   ├── app.py                   # router + guardas de sesión
│   ├── context.py               # dependencias y usuario por página
│   ├── base_controller.py       # contrato común (construir / ir)
│   ├── login_controller.py
│   ├── client_controller.py
│   ├── operations_controller.py
│   ├── history_controller.py
│   ├── staff_controller.py
│   └── client_form_controller.py
├── views/                       # CAPA VISTA (solo interfaz)
│   ├── login_view.py
│   ├── client_home_view.py
│   ├── operations_view.py
│   ├── history_view.py
│   ├── staff_home_view.py
│   ├── client_form_view.py
│   ├── components.py            # widgets reutilizables
│   ├── formatting.py            # formato de presentación
│   ├── theme.py                 # paleta de colores
│   └── view_models.py           # DTOs que consume la vista
└── models/                      # CAPA MODELO (negocio + persistencia)
    ├── orm.py                   # tablas SQLAlchemy
    ├── repositories.py          # DAO: único lugar con SQL
    ├── entities.py              # entidades puras del dominio
    └── services/
        ├── validaciones.py      # funciones puras de validación
        ├── auth_service.py      # login y rol
        ├── client_service.py    # alta/edición de clientes y cuentas
        └── operation_service.py # depósitos, retiros e historial
```

Los módulos históricos (`src/dao.py`, `src/autenticacion.py`, `src/models.py`)
quedan solo como **shims de compatibilidad** para no romper la suite de tests.

## Responsabilidad de cada capa

### Modelo — `src/models/`
- **Entidades** (`entities.py`): reglas del negocio (`Cuenta.depositar`,
  `SaldoInsuficienteError`, validaciones de `Persona`). No conocen Flet ni SQL.
- **Servicios** (`services/`): orquestan entidades y repositorio. Devuelven
  dataclasses o diccionarios con nombres explícitos, nunca tuplas posicionales.
- **Repositorio** (`repositories.py`): único punto que ejecuta SQL/SQLAlchemy.
- **Cero imports de Flet.**

### Vista — `src/views/`
- Solo **dibuja** controles y **captura clics**; avisa al controlador por callback.
- No consulta la base, no importa el DAO ni las entidades y no hace cuentas de negocio.
- Recibe **DTOs** (`CuentaVista`, `MovimientoVista`, `ClienteVista`,
  `ClienteFormVista`) ya preparados, para no acoplarse al dominio.

### Controlador — `src/controllers/`
- Intercepta los eventos de la vista y llama al servicio correcto.
- Maneja los errores con `try/except` y muestra mensajes en la UI.
- Traduce dominio → DTO de vista y actualiza la pantalla de forma reactiva.
- `App` es el router: construye cada controlador, aplica las guardas
  (`requiere_personal` / `requiere_cliente`) y monta el control en la `page`.
- El estado de sesión vive en `AppContext` (uno por página), no en un global.

## Flujo de una acción (ejemplo: depósito)

1. La **vista** captura el clic y llama a `on_ejecutar(id_cuenta, tipo, monto)`.
2. El **controlador** busca la cuenta, llama a `OperationService.depositar(...)`
   dentro de un `try/except`.
3. El **servicio** valida el monto, aplica la regla en la entidad
   (`cuenta.depositar`) y pide al **repositorio** que persista saldo + transacción.
4. El **repositorio** ejecuta el `UPDATE` y el `INSERT` en una sola transacción SQL.
5. El controlador recibe el saldo nuevo, limpia el campo y pide a la vista
   mostrar el aviso: la vista **nunca** tocó la base.

## Reglas de dependencia

| Capa        | Puede importar                          | No puede importar              |
|-------------|-----------------------------------------|--------------------------------|
| Vista       | `flet`, `views/*`                       | `models`, `controllers`, SQL   |
| Controlador | `views/*`, `models/services/*`          | SQL directo                    |
| Modelo      | entidades, `models/*`                   | `flet`, `views`, `controllers` |

## Ejecución y pruebas

```powershell
.\venv\Scripts\Activate.ps1
python main.py
pytest -q
```

Credenciales de la base versionada:
- Personal: DNI `22233344` / clave `admin123`
- Cliente: DNI `00233444` / clave `1234`
