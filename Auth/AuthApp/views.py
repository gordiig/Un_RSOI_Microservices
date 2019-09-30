from rest_framework import status
from rest_framework.views import Request, Response, APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from AuthApp.serializers import UserSerializer
from django.contrib.auth.models import User


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

    def patch(self, request: Request):
        if request.user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request):
        if request.user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UsersView(ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return User.objects.all()


class ConcreteUserView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request: Request, user_id):
        try:
            person = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(instance=person)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class RegisterView(APIView):
#     """
#     Вьюха для регистрации
#     """
#     def post(self, request: Request, *args, **kwargs):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
