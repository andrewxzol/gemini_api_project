import os
import google.generativeai as genai
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import GeminiImage
from .serializers import GeminiImageSerializer
from drf_spectacular.utils import extend_schema

# Налаштування Gemini API
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY is not set in environment variables.")


class GeminiImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        operation_id="upload_image",
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
            # 1. Збереження об'єкта в базу даних RDS
            instance = serializer.save()
            image_path = instance.image.path

            # 2. Формування ключа кешування
            cache_key = f"gemini_analysis_{instance.id}"

            # 3. Перевірка наявності результату в Redis
            cached_result = cache.get(cache_key)
            if cached_result:
                print(f"CACHE HIT: Loading analysis for image {instance.id} from Redis")
                instance.analysis_result = cached_result
                instance.save()
                return Response(GeminiImageSerializer(instance).data, status=status.HTTP_200_OK)

            # --- ВАЖЛИВО: Цей блок має бути НА ОДНОМУ РІВНІ з "if cached_result", а не всередині нього ---

            # 4. Виконання запиту до Gemini API, якщо кеш порожній
            print(f"API CALL: Requesting Gemini for image {instance.id}")
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')

                with open(image_path, 'rb') as f:
                    image_data = f.read()

                content = [
                    "Describe this image in detail.",
                    {"mime_type": "image/jpeg", "data": image_data}
                ]

                response = model.generate_content(content)
                analysis_text = response.text

                # 5. Зберігаємо результат у Redis на 24 години
                cache.set(cache_key, analysis_text, 86400)

                # 6. Оновлення запису в базі даних
                instance.analysis_result = analysis_text
                instance.save()

                return Response(GeminiImageSerializer(instance).data, status=status.HTTP_201_CREATED)

            except Exception as e:
                import traceback
                print(f"FULL ERROR:\n{traceback.format_exc()}")
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)