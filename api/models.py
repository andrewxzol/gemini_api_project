from django.db import models

class GeminiImage(models.Model):
    image = models.ImageField(upload_to='uploaded_images/')
    analysis_result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} - {self.created_at}"