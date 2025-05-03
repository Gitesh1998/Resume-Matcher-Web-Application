from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Match Resume Page
    path('match/', views.match_resumes, name='match_resumes'),
    path('match-result/', views.match_result, name='match_result'),
    path('upload/', views.upload_page, name='upload_page'),  # Upload Resume Page
    path('upload-resume/', views.upload_resume, name='upload_resume'),  # Resume POST handler
    path('resumes/', views.list_resumes, name='list_resumes'),
    path('resumes/delete/<str:filename>/', views.delete_resume, name='delete_resume'),
    path('logout/', views.logout_view, name='logout'),
]
