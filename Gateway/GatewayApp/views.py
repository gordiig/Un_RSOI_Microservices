from rest_framework.views import Response, Request, APIView
from GatewayApp.requesters import Requester
from GatewayApp.permissions import IsAuthenticatedThroughAuthService


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
