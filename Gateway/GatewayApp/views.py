from rest_framework.views import Response, Request, APIView
from GatewayApp.requesters.messages_requester import MessagesRequester
from GatewayApp.requesters.images_requester import ImagesRequester
from GatewayApp.requesters.audio_requester import AudioRequester
from GatewayApp.requesters.auth_requester import AuthRequester
from GatewayApp.permissions import IsAuthenticatedThroughAuthService


# MARK: - Auth
class BaseAuthView(APIView):
    REQUESTER = AuthRequester()


class AuthView(BaseAuthView):
    """
    Получение токена по юзернейму и паролю
    """
    def post(self, request: Request):
        response_json, code = self.REQUESTER.authenticate(data=request.data)
        return Response(response_json, status=code)


class RegisterView(BaseAuthView):
    """
    Регистрация
    """
    def post(self, request: Request):
        response_json, code = self.REQUESTER.register(request=request, data=request.data)
        return Response(data=response_json, status=code)


class GetUserInfoView(BaseAuthView):
    """
    Получение инфы о юзере по токену
    """
    permission_classes = (IsAuthenticatedThroughAuthService,)

    def get(self, request: Request):
        response_json, code = self.REQUESTER.get_user_info(request=request)
        return Response(response_json, status=code)

    def delete(self, request: Request):
        response_json, code = self.REQUESTER.delete_user(request=request)
        return Response(response_json, status=code)


class UsersView(BaseAuthView):
    """
    Получение списка юзеров
    """
    permission_classes = (IsAuthenticatedThroughAuthService,)

    def get(self, request: Request):
        response_json, code = self.REQUESTER.get_users(request=request)
        return Response(response_json, status=code)


class ConcreteUserView(BaseAuthView):
    """
    Получение конкретного пользователя
    """
    permission_classes = (IsAuthenticatedThroughAuthService,)

    def get(self, request: Request, user_id):
        response_json, code = self.REQUESTER.get_concrete_user(request=request, user_id=user_id)
        return Response(response_json, status=code)


# MARK: - Аудио
class BaseAudioView(APIView):
    REQUESTER = AudioRequester()


class AudiosView(BaseAudioView):
    """
    Получение всех аудио
    """
    permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request):
        data, code = self.REQUESTER.get_audios(request=request)
        return Response(data, status=code)

    def post(self, request: Request):
        data, code = self.REQUESTER.post_audio(request=request, data=request.data)
        return Response(data, status=code)


class ConcreteAudioView(BaseAudioView):
    """
    Получение определенного аудио
    """
    permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request, audio_uuid):
        data, code = self.REQUESTER.get_concrete_audio(request=request, uuid=audio_uuid)
        return Response(data, status=code)

    def patch(self, request: Request, audio_uuid):
        data, code = self.REQUESTER.patch_audio(request=request, uuid=audio_uuid, data=request.data)
        return Response(data, status=code)

    def delete(self, request: Request, audio_uuid):
        data, code = self.REQUESTER.delete_audio(request=request, uuid=audio_uuid)
        return Response(data, status=code)


# MARK: - Картинки
class BaseImageView(APIView):
    REQUESTER = ImagesRequester()


TOKEN = ''
REFRESH = ''


class ImagesView(BaseImageView):
    """
    Получение всех картинок
    """
    # permission_classes = (IsAuthenticatedThroughAuthService, )

    def _get_token(self, refresh=False):
        import requests
        global TOKEN, REFRESH
        body = {
            'server_id': 'Images_id',
            'server_secret': 'Images_secret',
        }
        if refresh:
            body['refresh_token'] = REFRESH
        ret = requests.post('http://127.0.0.1:8003/api/server_login/', json=body)
        print(ret.json())
        TOKEN = ret.json()['token']
        REFRESH = ret.json()['refresh_token']

    def get(self, request: Request):
        if TOKEN == '':
            self._get_token()
        data, code = self.REQUESTER.get_images(request=request)
        if code == 403:
            self._get_token(refresh=True)
        data, code = self.REQUESTER.get_images(request=request)
        return Response(data, status=code)

    def post(self, request: Request):
        if TOKEN == '':
            self._get_token()
        data, code = self.REQUESTER.post_image(request=request, data=request.data)
        if code == 403:
            self._get_token(refresh=True)
        data, code = self.REQUESTER.post_image(request=request, data=request.data)
        return Response(data, status=code)


class ConcreteImageView(BaseImageView):
    """
    Получение определенной картинки
    """
    permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request, image_uuid):
        data, code = self.REQUESTER.get_concrete_image(request=request, uuid=image_uuid)
        return Response(data, status=code)

    def patch(self, request: Request, image_uuid):
        data, code = self.REQUESTER.patch_image(request=request, uuid=image_uuid, data=request.data)
        return Response(data, status=code)

    def delete(self, request: Request, image_uuid):
        data, code = self.REQUESTER.delete_image(request=request, uuid=image_uuid)
        return Response(data, status=code)


# MARK: - Сообщения
class BaseMessageView(APIView):
    REQUESTER = MessagesRequester()


class MessagesView(BaseMessageView):
    """
    Получение всех картинок
    """
    permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request):
        data, code = self.REQUESTER.get_messages(request=request)
        return Response(data, status=code)

    def post(self, request: Request):
        data, code = self.REQUESTER.post_message(request=request, data=request.data)
        return Response(data, status=code)


class ConcreteMessageView(BaseMessageView):
    """
    Получение определенного сообещния
    """
    permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request, message_uuid):
        data, code = self.REQUESTER.get_concrete_message(request=request, uuid=message_uuid)
        return Response(data, status=code)

    def patch(self, request: Request, message_uuid):
        data, code = self.REQUESTER.patch_message(request=request, uuid=message_uuid, data=request.data)
        return Response(data, status=code)

    def delete(self, request: Request, message_uuid):
        data, code = self.REQUESTER.delete_message(request=request, uuid=message_uuid)
        return Response(data, status=code)


from django.shortcuts import redirect
from django.views import View
class OLoginView(View):
    """
    Логин в OAuth
    """
    def get(self, request):
        uri = 'http://127.0.0.1:8001/o/authorize/?client_id=Gateway_id&grant_type=authorization_code&response_type=token'
        return redirect(uri)


class ORedirectView(APIView):
    """
    Получение токена OAuth
    """
    def get(self, request: Request):
        import requests
        code = request.query_params['code']
        data_to_send = f'client_id=Gateway_id&client_secret=Gateway_secret&code={code}&grant_type=authorization_code'
        ret = requests.post(url='http://127.0.0.1:8001/o/token/', data=data_to_send,
                            headers={'content-type': 'application/x-www-form-urlencoded'})
        return Response(ret.json(), status=ret.status_code)
