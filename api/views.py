import os
import google.generativeai as genai
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import GeminiImage
from .serializers import GeminiImageSerializer

# Налаштування Gemini API
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY is not set in environment variables.")


class GeminiImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = GeminiImageSerializer(data=request.data)
        if serializer.is_valid():
            # 1. Збереження об'єкта в базу даних RDS
            instance = serializer.save()
            image_path = instance.image.path

            # 2. Формування ключа кешування (використовуємо ID запису)
            cache_key = f"gemini_analysis_{instance.id}"

            # 3. Перевірка наявності результату в Redis
            cached_result = cache.get(cache_key)
            if cached_result:
                print(f"CACHE HIT: Loading analysis for image {instance.id} from Redis")
                instance.analysis_result = cached_result
                instance.save()
                return Response(GeminiImageSerializer(instance).data, status=status.HTTP_200_OK)

            # 4. Виконання запиту до Gemini API, якщо кеш порожній
            print(f"API CALL: Requesting Gemini for image {instance.id}")
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')

                # Завантаження файлу в Gemini API
                sample_file = genai.upload_file(path=image_path, display_name=f"upload_{instance.id}")

                # Генерація контенту
                response = model.generate_content([sample_file, "Describe this image in detail."])
                analysis_text = response.text

                # 5. Збереження результату в Redis на 24 години (86400 секунд)
                cache.set(cache_key, analysis_text, 86400)

                # 6. Оновлення запису в базі даних
                instance.analysis_result = analysis_text
                instance.save()

                return Response(GeminiImageSerializer(instance).data, status=status.HTTP_201_CREATED)

            except Exception as e:
                print(f"ERROR: Gemini API call failed: {str(e)}")
                return Response({"error": "Failed to analyze image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)