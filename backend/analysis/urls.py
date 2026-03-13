from django.urls import path
from .views import ImageAnalysisViewSet

urlpatterns = [

    path('upload/', ImageAnalysisViewSet.as_view({'post': 'create'}), name='analysis-upload'),

    path('upload/<int:pk>/', ImageAnalysisViewSet.as_view({'get': 'retrieve'}), name='analysis-detail'),

]
