from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import UserRegistrationSerializer
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer


class UserRegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

def register_page(request):
    return render(request, 'register.html')


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Створюємо або отримуємо існуючий токен для цього юзера
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'username': user.username,
                'message': 'Вхід успішний'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)