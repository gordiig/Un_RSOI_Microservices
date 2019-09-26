from rest_framework import status
from rest_framework.views import Request, Response, APIView
from rest_framework.permissions import IsAuthenticated
from AuthApp.serializers import UserSerializer


class UserInfoGetterView(APIView):
    """
    Вьюха для получения информации о юзере
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request: Request, *args, **kwargs):
        if request.user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(APIView):
    """
    Вьюха для регистрации
    """
    def post(self, request: Request, *args, **kwargs):
        serializer = UserSerializer(instance=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)