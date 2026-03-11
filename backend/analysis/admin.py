from django.contrib import admin
from .models import GeminiImage, ImageAnalysis

@admin.register(GeminiImage)
class GeminiImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'analysis_result_summary')
    list_filter = ('created_at', 'user')
    readonly_fields = ('created_at',)

    def analysis_result_summary(self, obj):
        if obj.analysis_result:
            return obj.analysis_result[:50] + "..."
        return "Немає результату"
    analysis_result_summary.short_description = "Результат (коротко)"

@admin.register(ImageAnalysis)
class ImageAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'model_name', 'created_at')