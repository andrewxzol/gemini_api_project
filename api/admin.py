from django.contrib import admin
from .models import GeminiImage
from .models import TestModel

# Видаляємо декоратор і реєструємо вручну
class GeminiImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'created_at')
    readonly_fields = ('analysis_result', 'created_at')

admin.site.register(GeminiImage, GeminiImageAdmin)
print(f"!!! MODEL REGISTERED: {GeminiImage in admin.site._registry}")

admin.site.register(TestModel)