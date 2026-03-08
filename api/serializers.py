from rest_framework import serializers
from .models import GeminiImage

class GeminiImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeminiImage
        # Вказуємо, які поля ми хочемо бачити в API
        fields = ['id', 'image', 'analysis_result', 'created_at']
        # Поле analysis_result ми заповнимо самі після відповіді Gemini,
        # тому користувачу його присилати не треба (read_only)
        read_only_fields = ['analysis_result', 'created_at']