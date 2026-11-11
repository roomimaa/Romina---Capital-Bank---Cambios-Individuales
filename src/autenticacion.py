"""Compatibilidad: la autenticación real vive en ``AuthService``.

Se conserva este nombre porque la suite de tests y ``programa_dao.py`` lo usan.
"""

from src.models.services.auth_service import AuthService

Autenticacion = AuthService

__all__ = ["Autenticacion", "AuthService"]
