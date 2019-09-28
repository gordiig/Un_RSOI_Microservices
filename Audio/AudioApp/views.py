from rest_framework import status
from rest_framework.views import Response, Request, APIView
from rest_framework.generics import ListCreateAPIView
from AudioApp.serializers import AudioSerializer
from AudioApp.models import Audio


class AudiosView(ListCreateAPIView):
    """
    Вьюха для списка аудио
    """
    serializer_class = AudioSerializer

    def get_queryset(self):
        return Audio.objects.all()


class ConcreteAudioView(APIView):
    """
    Вьюха для конкретного аудио
    """
    def get(self, request: Request, audio_uuid):
        try:
            audio = Audio.objects.get(pk=audio_uuid)
        except Audio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AudioSerializer(instance=audio)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, audio_uuid):
        try:
            audio = Audio.objects.get(pk=audio_uuid)
        except Audio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        audio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
