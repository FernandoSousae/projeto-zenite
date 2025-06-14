# backend/core/permissions.py
from rest_framework import permissions

class IsInGroup(permissions.BasePermission):
    """
    Permissão customizada que permite acesso apenas a usuários
    que pertencem a um grupo específico.
    """
    def __init__(self, *groups):
        self.groups = groups

    def has_permission(self, request, view):
        # Verifica se o usuário está autenticado e pertence a um dos grupos necessários.
        return (
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name__in=self.groups).exists()
        )

    # Precisamos instanciar a classe na view, então redefinimos o __call__
    def __call__(self):
        return self