from rest_framework.views import Response, Request, APIView
from GatewayApp.requesters import Requester


# MARK: - Аудио
class AudiosView(APIView):
    """
    Получение всех аудио
    """
    def get(self, request: Request):
        data, code = Requester.get_audios()
        return Response(data, status=code)


class ConcreteAudioView(APIView):
    """
    Получение определенного аудио
    """
    def get(self, request: Request, audio_uuid):
        data, code = Requester.get_concrete_audio(str(audio_uuid))
        return Response(data, status=code)


# MARK: - Картинки
class ImagesView(APIView):
    """
    Получение всех картинок
    """
    def get(self, request: Request):
        data, code = Requester.get_images()
        return Response(data, status=code)


class ConcreteImageView(APIView):
    """
    Получение определенной картинки
    """
    def get(self, request: Request, image_uuid):
        data, code = Requester.get_concrete_image(str(image_uuid))
        return Response(data, status=code)


# MARK: - Сообщения
class MessagesView(APIView):
    """
    Получение всех картинок
    """
    def get(self, request: Request):
        data, code = Requester.get_messages()
        return Response(data, status=code)


class ConcreteMessageView(APIView):
    """
    Получение определенного сообещния
    """
    def get(self, request: Request, image_uuid):
        data, code = Requester.get_concrete_message(str(image_uuid))
        return Response(data, status=code)
