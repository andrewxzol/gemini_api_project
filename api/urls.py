from django.urls import path
from .views import GeminiImageUploadView

urlpatterns = [
    path('upload/', GeminiImageUploadView.as_view(), name='image-upload'),
]