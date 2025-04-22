from django.shortcuts import render, redirect
from .models import Resume, MatchResult
from .forms import ResumeUploadForm, JobDescriptionForm
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
import os
import re

def basic_text_match(resume_text, job_text):
    resume_words = set(re.findall(r'\w+', resume_text.lower()))
    job_words = set(re.findall(r'\w+', job_text.lower()))
    return len(resume_words & job_words) / len(job_words) * 100 if job_words else 0

@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resumes/dashboard.html', {'resumes': resumes})

@login_required
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.name = os.path.basename(resume.file.name)
            resume.save()
            return redirect('dashboard')
    return redirect('dashboard')

@login_required
def delete_resume(request, resume_id):
    Resume.objects.get(id=resume_id, user=request.user).delete()
    return redirect('dashboard')

@login_required
def match_resumes(request):
    if request.method == 'POST':
        form = JobDescriptionForm(request.POST)
        if form.is_valid():
            job_text = form.cleaned_data['description']
            resumes = Resume.objects.filter(user=request.user)
            results = []
            for resume in resumes:
                with resume.file.open('r') as f:
                    text = f.read()
                    score = basic_text_match(text, job_text)
                    result = MatchResult.objects.create(
                        resume=resume,
                        job_description=job_text,
                        match_percent=score,
                        matched_at=now()
                    )
                    results.append(result)
            results.sort(key=lambda x: x.match_percent, reverse=True)
            return render(request, 'resumes/match_results.html', {'results': results})
    return redirect('dashboard')
