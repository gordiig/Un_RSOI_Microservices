from rest_framework import status
from rest_framework.views import APIView, Response, Request
from rest_framework.generics import ListCreateAPIView
from django.db.models import Q
from MessagesApp.serializers import MessageSerializer
from MessagesApp.models import Message


class AllMessagesView(ListCreateAPIView):
    """
    Вьюха для вывода всех сообщений и добавления нового
    """
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.all()


class MessagesView(APIView):
    """
    Вьюха для вывода всех сообщений пользователя
    """
    def get(self, request: Request, user_id):
        msgs = Message.objects.filter(Q(from_user_id=user_id) | Q(to_user_id=user_id))
        if len(msgs) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(instance=msgs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ConcreteMessageView(APIView):
    """
    Вьюха для отображения конкретного сообщения
    """
    def get(self, request: Request, message_id):
        try:
            msg = Message.objects.get(pk=message_id)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(data=msg)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, message_id):
        try:
            msg = Message.objects.get(pk=message_id)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        msg.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
