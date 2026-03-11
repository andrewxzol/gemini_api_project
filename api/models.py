from django.db import models
from django.contrib.auth.models import User


class GeminiImage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='images',
        null=True,  # Дозволяємо порожнє значення для існуючих картинок
        blank=True
    )

    image = models.ImageField(upload_to='uploaded_images/')
    analysis_result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} - {self.created_at}"


class ImageAnalysis(models.Model):
    # Поле для завантаження файлу (зберігатиметься в папці media/uploads/)
    image = models.ImageField(upload_to='uploads/')

    # Текст відповіді, який ми отримаємо від Gemini
    analysis_result = models.TextField(blank=True, null=True)

    # Назва моделі, яку ми використовували (наприклад, gemini-1.5-flash-latest)
    model_name = models.CharField(max_length=100, default='models/gemini-flash-latest')

    # Дата та час створення запису (автоматично при збереженні)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

