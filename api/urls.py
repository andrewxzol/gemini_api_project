from django.urls import path
from .views import GeminiImageUploadView
from .views import UserRegisterView
from .views import register_page

urlpatterns = [
    path('upload/', GeminiImageUploadView.as_view(), name='image-upload'),
    path('registration/', UserRegisterView.as_view(), name='registration'),
    path('join/', register_page, name='register-ui'),
]