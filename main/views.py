# from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate, logout, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer, ProfileSerializer
import jsonpickle
# Create your views here.


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def index(req):
    return Response({"Welcome to user system"}, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class RegisterUserView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def user_login(req):
    email = req.data.get("email")
    password = req.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Enter email/password'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)
    if not user:
        return Response({'error': 'Incorrect email/password'}, status=status.HTTP_400_BAD_REQUEST)

    login(req, user)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_logout(req):
    req.user.auth_token.delete()
    logout(req)
    return Response({'message': 'Logout Success'}, status=status.HTTP_200_OK)


class UpdateProfileView(UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_user_model().objects.get(id=self.request.user.id)
