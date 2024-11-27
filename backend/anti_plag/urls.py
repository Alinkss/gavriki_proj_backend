from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.report_view, name='report'),
    path('analysis_text/', views.analysis_text, name='analysis_text'),
]
