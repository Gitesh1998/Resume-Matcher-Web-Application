

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_resume, name='upload_resume'),
    path('match/', views.match_resumes, name='match_resumes'),
    path('', views.dashboard, name='dashboard'),
    path('resumes/', views.list_resumes, name='list_resumes'),
    path('resumes/delete/<str:filename>/', views.delete_resume, name='delete_resume'),
    path('about/', views.about_view, name='about'),
    path('signup/', views.signup_view, name='signup'),
]
