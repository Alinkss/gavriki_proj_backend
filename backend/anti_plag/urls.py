from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.report_view, name='report'),
    path('analysis_text/', views.analysis_text, name='analysis_text'),
    path('human_or_ai/', views.human_or_ai, name='human_or_ai'),
    # path('classify_ai_human/', views.classify_ai_human, name='classify_ai_human'),
]
