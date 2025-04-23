from django.shortcuts import render, redirect
from .models import Resume, MatchResult
from .forms import ResumeUploadForm, JobDescriptionForm
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import re
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .resume_matcher import match_resume_to_job


# ✅ Use this helper function
def get_uploaded_resumes_dir():
    path = os.path.join(settings.MEDIA_ROOT, 'resumes')
    os.makedirs(path, exist_ok=True)
    return path


@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resumes/dashboard.html', {'resumes': resumes})


@login_required
def upload_resume(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        resume_file = request.FILES['resume']
        upload_dir = get_uploaded_resumes_dir()
        fs = FileSystemStorage(location=upload_dir)
        fs.save(resume_file.name, resume_file)

    return redirect('dashboard')


@login_required
def match_resumes(request):
    matched_resume = None
    if request.method == 'POST':
        job_desc = request.POST['job_description']
        upload_dir = get_uploaded_resumes_dir()
        matched_resume = match_resume_to_job(job_desc, upload_dir)

    return render(request, 'resumes/dashboard.html', {
        'matched_resume': matched_resume
    })


@login_required
def delete_resume(request, resume_id):
    Resume.objects.get(id=resume_id, user=request.user).delete()
    return redirect('dashboard')
