"""Compatibilidad: el repositorio real vive en ``src.models.repositories``.

Se mantiene este módulo para no romper imports históricos (tests, scripts de
demostración y documentación). El código nuevo debe importar desde
``src.models``.
"""

from src.models.repositories import DAO, pwd_context

__all__ = ["DAO", "pwd_context"]
