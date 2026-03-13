import os
import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import GeminiImageSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from .tasks import analyze_image_task
from .models import ImageAnalysis
from django.db import transaction

# Налаштування Gemini API
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY is not set in environment variables.")


class GeminiImageUploadView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        operation_id="upload_image",
        summary="Завантажити зображення для асинхронного аналізу",
        description="Зберігає зображення та запускає фонову задачу в Celery. Результат з'явиться в полі analysis_result згодом.",
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'image': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        },
        responses={201: GeminiImageSerializer},
    )

    def post(self, request, *args, **kwargs):
        serializer = GeminiImageSerializer(data=request.data)
        if serializer.is_valid():
            # 1. Тільки зберігаємо в БД
            instance = serializer.save(user=request.user)

            # 2. Віддаємо ID задачі в Celery.
            # ВСЯ магія (Gemini, Redis, Hash) тепер буде в tasks.py
            analyze_image_task.delay(instance.id)

            # 3. Миттєво відповідаємо користувачу
            return Response({
                "id": instance.id,
                "status": "Processing",
                "message": "Image uploaded. Analysis started in background."
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageAnalysisViewSet(viewsets.ModelViewSet):
    queryset = ImageAnalysis.objects.all()
    serializer_class = GeminiImageSerializer

    def perform_create(self, serializer):
        # 1. Зберігаємо запис у базу (створюємо об'єкт)
        instance = serializer.save(user=self.request.user)

        # 2. Відправляємо ID об'єкта в Celery
        # Як тільки ти допишеш цей рядок, імпорт зверху стане активним!
        transaction.on_commit(lambda: analyze_image_task.delay(instance.id))