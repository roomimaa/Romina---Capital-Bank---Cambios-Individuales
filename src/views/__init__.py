"""Capa de VISTA: pantallas Flet que solo dibujan y capturan clics."""

from src.views.client_form_view import ClientFormView
from src.views.client_home_view import ClientHomeView
from src.views.history_view import HistoryView
from src.views.login_view import LoginView
from src.views.operations_view import OperationsView
from src.views.staff_home_view import StaffHomeView

__all__ = [
    "ClientFormView",
    "ClientHomeView",
    "HistoryView",
    "LoginView",
    "OperationsView",
    "StaffHomeView",
]
