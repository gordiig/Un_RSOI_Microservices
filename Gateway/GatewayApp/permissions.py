from rest_framework.permissions import BasePermission
from GatewayApp.requesters import Requester


class IsAuthenticatedThroughAuthService(BasePermission):
    """
    Пермишн класс для проверки токена на стороне Auth-сервиса
    """
    def has_permission(self, request, view):
        token_str = request.META.get('HTTP_AUTHORIZATION')
        if not token_str:
            return False
        token = token_str[6:]
        _, code = Requester.get_user_info(token)
        return code == 200
