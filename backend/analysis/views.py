import os
import google.generativeai as genai
import hashlib
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import GeminiImageSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication



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
            instance = serializer.save(user=request.user)
            image_path = instance.image.path

            # Створюємо хеш файлу, щоб впізнати однакові картинки
            with open(image_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()

            # ВИПРАВЛЕНО: Використовуємо хеш як ключ кешу
            cache_key = f"gemini_hash_{file_hash}"

            # 3. Перевірка наявності результату в Redis
            cached_result = cache.get(cache_key)
            if cached_result:
                print(f"CACHE HIT: Loading analysis for hash {file_hash} from Redis")
                instance.analysis_result = cached_result
                instance.save()
                return Response(GeminiImageSerializer(instance).data, status=status.HTTP_200_OK)

            # 4. Виконання запиту до Gemini API
            print(f"API CALL: Requesting Gemini for new image content (hash: {file_hash})")
            try:
                # Зверни увагу: якщо gemini-2.5-flash видасть помилку 404,
                # заміни на gemini-1.5-flash, оскільки 2.5 може бути в preview
                model = genai.GenerativeModel('models/gemini-2.5-flash')

                with open(image_path, 'rb') as f:
                    image_data = f.read()

                content = [
                    "Describe this image in detail.",
                    {"mime_type": "image/jpeg", "data": image_data}
                ]

                response = model.generate_content(content)
                analysis_text = response.text

                # 5. Зберігаємо за хешем у Redis на 24 години
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
