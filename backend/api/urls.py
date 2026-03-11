from django.urls import path, include

urlpatterns = [
    # Все, що стосується юзерів (login, register) буде йти через /api/auth/
    path('auth/', include('backend.accounts.urls')),

    # Все, що стосується Gemini буде йти через /api/analysis/
    path('analysis/', include('backend.analysis.urls')),
]