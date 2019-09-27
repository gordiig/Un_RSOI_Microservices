from rest_framework import status
from rest_framework.views import Response, Request, APIView
from rest_framework.generics import ListCreateAPIView
from ImagesApp.models import Image
from ImagesApp.serializers import ImageSerializer


class ImagesView(ListCreateAPIView):
    """
    Вьюха для списка изображений
    """
    def get_queryset(self):
        return Image.objects.all()


class ConcreteImageView(APIView):
    """
    Вьюха для конкретного изображения
    """
    def get(self, request: Request, image_uuid):
        try:
            img = Image.objects.get(pk=image_uuid)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ImageSerializer(instance=img)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, image_uuid):
        try:
            img = Image.objects.get(pk=image_uuid)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        img.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
