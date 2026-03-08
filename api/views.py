import google.generativeai as genai
import os
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import GeminiImage
from .serializers import GeminiImageSerializer
from django.conf import settings

# Налаштовуємо Gemini API ключем з нашого .env файлу
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("WARNING: GEMINI_API_KEY is not set in environment variables!")
genai.configure(api_key=api_key)


class ImageAnalysisView(APIView):
    @extend_schema(
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
        }
    )
    def post(self, request, *args, **kwargs):
        # 1. Приймаємо дані через серіалізатор
        serializer = GeminiImageSerializer(data=request.data)

        if serializer.is_valid():
            # 2. Зберігаємо об'єкт у базу (поки без аналізу)
            instance = serializer.save()

            try:
                # 3. Готуємо модель Gemini
                # 'gemini-1.5-flash' — швидка модель, що вміє читати картинки
                model = genai.GenerativeModel('models/gemini-2.5-flash')

                # Відкриваємо файл, який щойно зберігся на диск
                img_path = instance.image.path
                with open(img_path, 'rb') as f:
                    image_data = f.read()

                # 4. Відправляємо запит до Gemini
                # Ми передаємо список: текст-запит та саму картинку
                response = model.generate_content(
                    [
                        "Опиши, що ти бачиш на цьому зображенні українською мовою.",
                        {'mime_type': 'image/jpeg', 'data': image_data}
                    ],
                    request_options={"timeout": 600}  # Додаємо тут, через кому після списку
                )


                # 5. Зберігаємо відповідь від Gemini в базу
                instance.analysis_result = response.text
                instance.save()

                # Повертаємо оновлені дані користувачу
                return Response(GeminiImageSerializer(instance).data, status=status.HTTP_201_CREATED)

            except Exception as e:
                # Якщо щось пішло не так (наприклад, ключ не підійшов)
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)