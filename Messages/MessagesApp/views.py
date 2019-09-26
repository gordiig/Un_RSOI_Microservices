from rest_framework import status
from rest_framework.views import APIView, Response, Request
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from MessagesApp.serializers import MessageSerializer, ConcreteMessageSerializer
from MessagesApp.models import Message


class AllMessagesView(ListAPIView):
    """
    Вьюха для вывода всех сообщений (просто для наглядности, понятно что это плохо)
    """
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.all()


class MessagesView(APIView):
    """
    Вьюха для вывода всех сообщений пользователя
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = MessageSerializer

    def get_queryset(self, request: Request, *args, **kwargs):
        query_params = request.query_params
        try:


    def post(self, request: Request, *args, **kwargs):
        pass
