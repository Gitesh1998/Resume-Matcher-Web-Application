

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_resume, name='upload_resume'),
    path('match/', views.match_resumes, name='match_resumes'),
    path('', views.dashboard, name='dashboard'),
]
