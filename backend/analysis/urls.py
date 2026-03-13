from django.urls import path
from .views import ImageAnalysisViewSet

urlpatterns = [

    path('upload/', ImageAnalysisViewSet.as_view(), name='analysis-upload'),

]
