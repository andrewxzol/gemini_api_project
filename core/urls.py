from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # ПРАВИЛЬНИЙ ШЛЯХ: тепер шлемо запити в backend/api/urls.py
    path('api/', include('backend.api.urls')),

    # Swagger (документація) - залишаємо як є
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # UI сторінки
    path('dashboard/', TemplateView.as_view(template_name='index.html'), name='main-dashboard'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login-ui'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register-ui'),
]

# Важливо додати для роботи з картинками в медіа-папці
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
