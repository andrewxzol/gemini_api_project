import os
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db import transaction

# Імпортуємо тільки те, що реально використовуємо
from .models import ImageAnalysis
from .serializers import ImageAnalysisSerializer
from .tasks import analyze_image_task


class ImageAnalysisViewSet(viewsets.ModelViewSet):
    """
    Цей клас замінює собою і View, і APIView.
    Він автоматично підтримує GET (список), POST (створення), GET/ID (деталі).
    """
    queryset = ImageAnalysis.objects.all()
    serializer_class = ImageAnalysisSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 1. Зберігаємо об'єкт.
        # УВАГА: Якщо в моделі ImageAnalysis немає поля 'user',
        # прибери 'user=self.request.user'
        instance = serializer.save()

        # 2. Безпечний запуск таска після запису в RDS
        transaction.on_commit(lambda: analyze_image_task.delay(instance.id))

    # Кастомна відповідь після створення (щоб було як у твоєму APIView)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        instance = serializer.instance
        return Response({
            "id": instance.id,
            "status": "Processing",
            "message": "Image uploaded. Analysis started in background.",
            "image_url": request.build_absolute_uri(instance.image.url) if instance.image else None
        }, status=status.HTTP_201_CREATED)