from rest_framework.permissions import BasePermission
from GatewayApp.requesters.auth_requester import AuthRequester


class IsAuthenticatedThroughAuthService(BasePermission):
    """
    Пермишн класс для проверки токена на стороне Auth-сервиса
    """
    def has_permission(self, request, view):
        _, code = AuthRequester().get_user_info(request=request)
        return code == 200
