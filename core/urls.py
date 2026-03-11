from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), # Підключаємо наш додаток
    
    # Swagger (документація)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Головна сторінка
    path('dashboard/', TemplateView.as_view(template_name='index.html'), name='main-dashboard'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login-ui'),
]