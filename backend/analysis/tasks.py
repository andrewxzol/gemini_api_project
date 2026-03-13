import hashlib
import os
from django.core.cache import cache
from celery import shared_task
import google.generativeai as genai

@shared_task
def analyze_image_task(instance_id):
    from .models import ImageAnalysis  # Імпортуємо тут

    try:
        instance = ImageAnalysis.objects.get(id=instance_id)
        image_path = instance.image.path

        # --- Логіка з хешем ---
        with open(image_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()

        cache_key = f"gemini_hash_{file_hash}"
        cached_result = cache.get(cache_key)

        if cached_result:
            instance.analysis_result = cached_result
            instance.save()
            return "Loaded from cache"

        # --- Логіка з Gemini ---
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        # Порада: gemini-2.5-flash може бути нестабільним, 1.5-flash надійніше
        model = genai.GenerativeModel('models/gemini-flash-latest')

        with open(image_path, 'rb') as f:
            image_data = f.read()

        content = [
            "Describe this image in detail.",
            {"mime_type": "image/jpeg", "data": image_data}
        ]

        response = model.generate_content(content)
        analysis_text = response.text

        # Зберігаємо в Redis та в БД
        cache.set(cache_key, analysis_text, 86400)
        instance.analysis_result = analysis_text
        instance.save()

        return "Analysis completed"

    except Exception as e:
        # Логуємо помилку, щоб бачити її в `docker compose logs -f celery`
        print(f"ERROR in task: {str(e)}")
        return f"Error: {str(e)}"