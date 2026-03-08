from django.contrib import admin
from .models import GeminiImage
print("ADMIN FILE LOADED")
@admin.register(GeminiImage)
class GeminiImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'created_at')
    readonly_fields = ('analysis_result', 'created_at')