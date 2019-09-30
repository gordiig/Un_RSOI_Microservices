from rest_framework.views import Response, Request, APIView
from GatewayApp.requesters import Requester
from GatewayApp.permissions import IsAuthenticatedThroughAuthService


# MARK: - Auth
class AuthView(APIView):
    """
    Получение токена по юзернейму и паролю
    """
    def post(self, request: Request):
        response_json, code = Requester.authenticate(data=request.data)
        return Response(response_json, status=code)


class RegisterView(APIView):
    """
    Регистрация
    """
    def post(self, request: Request):
        response_json, code = Requester.register(data=request.data)
        return Response(data=response_json, status=code)


class GetUserInfoView(APIView):
    """
    Получение инфы о юзере по токену
    """
    permission_classes = (IsAuthenticatedThroughAuthService,)

    def get(self, request: Request):
        token_str = request.META.get('HTTP_AUTHORIZATION')
        if token_str is None:
            return Response({'error': 'No Authorization header!'}, status=400)
        token = token_str[6:]
        response_json, code = Requester.get_user_info(token)
        return Response(response_json, status=code)

    def delete(self, request: Request):
        token_str = request.META.get('HTTP_AUTHORIZATION')
        if token_str is None:
            return Response({'error': 'No Authorization header!'}, status=400)
        token = token_str[6:]
        response_json, code = Requester.delete_user(token)
        return Response(response_json, status=code)


class UsersView(APIView):
    """
    Получение списка юзеров
    """
    permission_classes = (IsAuthenticatedThroughAuthService,)

    def get(self, request: Request):
        token_str = request.META.get('HTTP_AUTHORIZATION')
        if token_str is None:
            return Response({'error': 'No Authorization header!'}, status=400)
        token = token_str[6:]
        limit_offset = request.query_params.get('limit'), request.query_params.get('offset')
        if limit_offset[0] is None or limit_offset[1] is None:
            limit_offset = None
        response_json, code = Requester.get_users(token, limit_offset)
        return Response(response_json, status=code)


class ConcreteUserView(APIView):
    """
    Получение конкретного пользователя
    """
    permission_classes = (IsAuthenticatedThroughAuthService,)

    def get(self, request: Request, user_id):
        token_str = request.META.get('HTTP_AUTHORIZATION')
        if token_str is None:
            return Response({'error': 'No Authorization header!'}, status=400)
        token = token_str[6:]
        response_json, code = Requester.get_concrete_user(token, user_id)
        return Response(response_json, status=code)


# MARK: - Аудио
class AudiosView(APIView):
    """
    Получение всех аудио
    """
    permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request):
        limit_offset = request.query_params.get('limit'), request.query_params.get('offset')
        if limit_offset[0] is None or limit_offset[1] is None:
            limit_offset = None
        data, code = Requester.get_audios(limit_and_offset=limit_offset)
        return Response(data, status=code)

    def post(self, request: Request):
        data, code = Requester.post_audio(request.data)
        return Response(data, status=code)


class ConcreteAudioView(APIView):
    """
    Получение определенного аудио
    """
    permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request, audio_uuid):
        data, code = Requester.get_concrete_audio(str(audio_uuid))
        return Response(data, status=code)

    def patch(self, request: Request, audio_uuid):
        data, code = Requester.patch_audio(str(audio_uuid), request.data)
        return Response(data, status=code)

    def delete(self, request: Request, audio_uuid):
        data, code = Requester.delete_audio(str(audio_uuid))
        return Response(data, status=code)


# MARK: - Картинки
class ImagesView(APIView):
    """
    Получение всех картинок
    """
    permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request):
        limit_offset = request.query_params.get('limit'), request.query_params.get('offset')
        if limit_offset[0] is None or limit_offset[1] is None:
            limit_offset = None
        data, code = Requester.get_images(limit_and_offset=limit_offset)
        return Response(data, status=code)

    def post(self, request: Request):
        data, code = Requester.post_image(request.data)
        return Response(data, status=code)


class ConcreteImageView(APIView):
    """
    Получение определенной картинки
    """
    permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request, image_uuid):
        data, code = Requester.get_concrete_image(str(image_uuid))
        return Response(data, status=code)

    def patch(self, request: Request, image_uuid):
        data, code = Requester.patch_image(str(image_uuid), request.data)
        return Response(data, status=code)

    def delete(self, request: Request, image_uuid):
        data, code = Requester.delete_image(str(image_uuid))
        return Response(data, status=code)


# MARK: - Сообщения
class MessagesView(APIView):
    """
    Получение всех картинок
    """
    permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request):
        # Getting token
        token_str = request.META.get('HTTP_AUTHORIZATION')
        if token_str is None:
            return Response({'error': 'No Authorization header!'}, status=400)
        token = token_str[6:]
        # Getting limit/offset
        limit_offset = request.query_params.get('limit'), request.query_params.get('offset')
        if limit_offset[0] is None or limit_offset[1] is None:
            limit_offset = None
        # Getting messages
        data, code = Requester.get_messages(token=token, limit_and_offset=limit_offset)
        return Response(data, status=code)

    def post(self, request: Request):
        token_str = request.META.get('HTTP_AUTHORIZATION')
        if token_str is None:
            return Response({'error': 'No Authorization header!'}, status=400)
        token = token_str[6:]
        data, code = Requester.post_message(token, request.data)
        return Response(data, status=code)


class ConcreteMessageView(APIView):
    """
    Получение определенного сообещния
    """
    permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request, message_uuid):
        data, code = Requester.get_concrete_message(str(message_uuid))
        return Response(data, status=code)

    def patch(self, request: Request, message_uuid):
        token_str = request.META.get('HTTP_AUTHORIZATION')
        if token_str is None:
            return Response({'error': 'No Authorization header!'}, status=400)
        token = token_str[6:]
        data, code = Requester.patch_message(token, str(message_uuid), request.data)
        return Response(data, status=code)

    def delete(self, request: Request, message_uuid):
        data, code = Requester.delete_message(str(message_uuid))
        return Response(data, status=code)
