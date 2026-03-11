from django.urls import path
from django.views.generic import TemplateView
from .views import (
    UserRegisterView,
    UserLoginView,
    register_page
)

urlpatterns = [
    # --- HTML Сторінки (UI) ---
    path('join/', register_page, name='register-ui'),
    path('login-page/', TemplateView.as_view(template_name='login.html'), name='login-ui'),

    # --- API Ендпоінти (сюди JS шле дані) ---
    path('register/', UserRegisterView.as_view(), name='api-register'),
    path('login/', UserLoginView.as_view(), name='api-login'),
]