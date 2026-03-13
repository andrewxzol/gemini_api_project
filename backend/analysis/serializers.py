from rest_framework import serializers
from .models import ImageAnalysis

class ImageAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageAnalysis
        fields = ['id', 'image', 'analysis_result', 'created_at']
        read_only_fields = ['analysis_result', 'created_at']