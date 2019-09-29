from rest_framework.views import Response, Request, APIView
from GatewayApp.requesters import Requester
from GatewayApp.permissions import IsAuthenticatedThroughAuthService


# MARK: - Auth
class AuthView(APIView):
    """
    Получение токена по юзернейму и паролю
    """
    def post(self, request: Request):
        if {'username', 'password'}.intersection(request.data.keys()) != 2:
            return Response({'error': 'Body must have username and password fields'}, status=400)
        response_json, code = Requester.authenticate(username=request.data['username'],
                                                     password=request.data['password'])
        return Response(response_json, status=code)


class RegisterView(APIView):
    """
    Регистрация
    """
    def post(self, request: Request):
        needed_data = {'username', 'password', 'email'}.intersection(request.data.keys())
        if len(needed_data) != 3:
            return Response({'error': 'Body must have username, email and password fields'}, status=400)
        response_json, code = Requester.register(username=request.data['username'], password=request.data['password'],
                                                 email=request.data['email'])
        return Response(data=response_json, status=code)


class GetUserInfoView(APIView):
    """
    Получение инфы о юзере по токену
    """
    def get(self, request: Request):
        token_str = request.META.get('Authorization')
        if token_str is None:
            return Response({'error': 'No Authorization header!'}, status=400)
        token = token_str[6:]
        response_json, code = Requester.get_user_info(token)
        return Response(response_json, status=code)


# MARK: - Аудио
class AudiosView(APIView):
    """
    Получение всех аудио
    """
    permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request):
        data, code = Requester.get_audios()
        return Response(data, status=code)


class ConcreteAudioView(APIView):
    """
    Получение определенного аудио
    """
    permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request, audio_uuid):
        data, code = Requester.get_concrete_audio(str(audio_uuid))
        return Response(data, status=code)


# MARK: - Картинки
class ImagesView(APIView):
    """
    Получение всех картинок
    """
    permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request):
        data, code = Requester.get_images()
        return Response(data, status=code)


class ConcreteImageView(APIView):
    """
    Получение определенной картинки
    """
    permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request, image_uuid):
        data, code = Requester.get_concrete_image(str(image_uuid))
        return Response(data, status=code)


# MARK: - Сообщения
class MessagesView(APIView):
    """
    Получение всех картинок
    """
    permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request):
        data, code = Requester.get_messages()
        return Response(data, status=code)


class ConcreteMessageView(APIView):
    """
    Получение определенного сообещния
    """
    permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request, image_uuid):
        data, code = Requester.get_concrete_message(str(image_uuid))
        return Response(data, status=code)
