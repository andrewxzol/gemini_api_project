from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import GeminiImage

@admin.register(GeminiImage)
class GeminiImageAdmin(admin.ModelAdmin):
    # Визначаємо, які колонки показувати в списку
    list_display = ('id', 'image', 'created_at')
    # Додаємо можливість перегляду результату аналізу
    readonly_fields = ('analysis_result', 'created_at')