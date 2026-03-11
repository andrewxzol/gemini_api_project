from django.urls import path
from django.views.generic import TemplateView
from .views import (
    GeminiImageUploadView,
    UserRegisterView,
    UserLoginView,  # Переконайся, що ти імпортував створену View для логіну
    register_page
)

urlpatterns = [
    # --- API (JSON відповіді) ---
    path('upload/', GeminiImageUploadView.as_view(), name='api-upload'),
    path('registration/', UserRegisterView.as_view(), name='api-registration'),
    path('login-api/', UserLoginView.as_view(), name='api-login'),  # Ендпоінт для отримання токена

    # --- UI (HTML сторінки) ---
    # Сторінка реєстрації (твоя існуюча)
    path('join/', register_page, name='register-ui'),

    # Сторінка входу
    path('login/', TemplateView.as_view(template_name='login.html'), name='login-ui'),

    # Головна сторінка (Dashboard)
    path('dashboard/', TemplateView.as_view(template_name='index.html'), name='dashboard-ui'),
]