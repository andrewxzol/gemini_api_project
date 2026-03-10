from django.urls import path
from .views import GeminiImageUploadView
from .views import UserRegisterView

urlpatterns = [
    path('upload/', GeminiImageUploadView.as_view(), name='image-upload'),
    path('registration/', UserRegisterView.as_view(), name='registration')
]