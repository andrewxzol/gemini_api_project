from django.contrib.auth.models import User
from rest_framework import serializers
from .models import GeminiImage
from django.contrib.auth import authenticate

class GeminiImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeminiImage
        # Вказуємо, які поля ми хочемо бачити в API
        fields = ['id', 'image', 'analysis_result', 'created_at']
        # Поле analysis_result ми заповнимо самі після відповіді Gemini,
        # тому користувачу його присилати не треба (read_only)
        read_only_fields = ['analysis_result', 'created_at']

class UserRegistrationSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True)

        class Meta:
            model = User
            fields = ['username', 'email', 'password']

        def create(self, validated_data):
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data.get('email', ''),
                password=validated_data['password']
            )
            return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Невірний логін або пароль')
        else:
            raise serializers.ValidationError('Потрібно ввести логін та пароль')

        data['user'] = user
        return data