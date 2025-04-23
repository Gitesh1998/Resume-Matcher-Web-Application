from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_resume, name='upload_resume'),
    path('delete/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('match/', views.match_resumes, name='match_resumes'),
    path('about/', views.about_view, name='about'),
    path('signup/', views.signup_view, name='signup'),
]
