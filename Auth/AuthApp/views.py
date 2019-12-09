from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import Request, Response, APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.authtoken.models import Token
from oauth2_provider.contrib.rest_framework.permissions import IsAuthenticatedOrTokenHasScope
from AuthApp.serializers import UserSerializer
from django.contrib.auth.models import User


@method_decorator(csrf_exempt, name='dispatch')
class LogInForOAuth2(View):
    def get(self, request):
        return render(request, template_name='AuthApp/logIn.html')

    def post(self, request: HttpRequest):
        try:
            username = request.POST['username']
            password = request.POST['password']
        except KeyError:
            import json
            return HttpResponseBadRequest(json.dumps({'error': 'wrong form data'}))
        user = authenticate(request, username=username, password=password)
        if user is None:
            return redirect(request.get_raw_uri())
        login(request, user)
        ret = redirect(f'http://{request.get_host()}{request.GET["next"]}')
        return ret


class UserInfoGetterView(APIView):
    """
    Вьюха для получения информации о юзере
    """
    permission_classes = (IsAuthenticatedOrTokenHasScope, )
    required_scopes = ('read', 'write')

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
    permission_classes = (IsAuthenticatedOrTokenHasScope, )
    required_scopes = ('read', )

    def get_queryset(self):
        return User.objects.all()


class ConcreteUserView(APIView):
    permission_classes = (IsAuthenticatedOrTokenHasScope, )

    def get(self, request: Request, user_id):
        try:
            person = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(instance=person)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(APIView):
    """
    Вьюха для регистрации
    """
    def post(self, request: Request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
