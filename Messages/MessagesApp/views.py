from rest_framework import status
from rest_framework.views import APIView, Response, Request
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Q
from MessagesApp.serializers import MessageSerializer
from MessagesApp.models import Message


class AllMessagesView(APIView):
    """
    Вьюха для вывода всех сообщений и добавления нового
    """
    def get(self, request: Request):
        try:
            user_id = request.query_params['user_id']
        except KeyError:
            return Response({'error': 'Wrong query params'}, status=status.HTTP_400_BAD_REQUEST)
        msgs = Message.objects.filter(Q(from_user_id=user_id) | Q(to_user_id=user_id))
        if len(msgs) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            _ = request.query_params['limit']
            paginator = LimitOffsetPagination()
            results = paginator.paginate_queryset(msgs, request)
        except KeyError:
            results = msgs
        serializer = MessageSerializer(instance=results, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConcreteMessageView(APIView):
    """
    Вьюха для отображения конкретного сообщения
    """
    def get(self, request: Request, message_uuid):
        try:
            msg = Message.objects.get(pk=message_uuid)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(instance=msg)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, message_uuid):
        try:
            msg = Message.objects.get(pk=message_uuid)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        msg.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
