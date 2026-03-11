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

    image = models.ImageField(upload_to='uploads/')
    analysis_result = models.TextField(blank=True, null=True)
    model_name = models.CharField(max_length=100, default='models/gemini-flash-latest')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

