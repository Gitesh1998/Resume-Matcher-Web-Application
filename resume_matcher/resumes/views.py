from django.shortcuts import render, redirect, get_object_or_404
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
from django.contrib.auth import logout

from .resume_matcher import match_resume_to_job


# ✅ Use this helper function
# def get_uploaded_resumes_dir():
#     path = os.path.join(settings.MEDIA_ROOT, 'resumes')
#     os.makedirs(path, exist_ok=True)
#     return path


from django.contrib.auth.forms import UserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after signup
    else:
        form = UserCreationForm()
    return render(request, 'resumes/signup.html', {'form': form})

def get_uploaded_resumes_dir(user_id):
    path = os.path.join(settings.MEDIA_ROOT, 'resumes', str(user_id))
    os.makedirs(path, exist_ok=True)
    return path



@login_required
def dashboard(request):
    print("DASHBOARD VIEW CALLED")
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resumes/dashboard.html', {'resumes': resumes})



def upload_resume(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        resume_file = request.FILES['resume']
        
        # Get upload directory for this user
        upload_dir = get_uploaded_resumes_dir(request.user.id)
        
        # Save the uploaded file
        fs = FileSystemStorage(location=upload_dir)
        fs.save(resume_file.name, resume_file)

    return redirect('dashboard')


# @login_required
# def match_resumes(request):
#     matched_resume = None
#     if request.method == 'POST':
#         job_desc = request.POST['job_description']
#         upload_dir = get_uploaded_resumes_dir()
#         matched_resume = match_resume_to_job(job_desc, upload_dir)

#     return render(request, 'resumes/dashboard.html', {
#         'matched_resume': matched_resume
#     })

@login_required
@login_required
def match_resumes(request):
    if request.method == 'POST':
        job_desc = request.POST['job_description']
        user = request.user
        upload_dir = get_uploaded_resumes_dir(user.id)
        matched_resume = match_resume_to_job(job_desc, upload_dir)

        if matched_resume:
            request.session['matched_resume'] = matched_resume  # Save result for next page
        return redirect('match_result')

    return redirect('dashboard')



# def match_resumes(request):
#     matched_resume = None
#     if request.method == 'POST':
#         # grab the job description
#         job_desc = request.POST['job_description']
        
#         # print user info to local console
#         user = request.user
#         print(f'User ID: {user.id}, Username: {user.username}')
        
#         # do your matching
#         upload_dir = get_uploaded_resumes_dir(user.id)
#         matched_resume = match_resume_to_job(job_desc, upload_dir)

#     return render(request, 'resumes/dashboard.html', {
#         'matched_resume': matched_resume
#     })


@login_required
def delete_resume(request, resume_id):
    Resume.objects.get(id=resume_id, user=request.user).delete()
    return redirect('dashboard')

@login_required
def list_resumes(request):
    upload_dir = get_uploaded_resumes_dir(request.user.id)
    file_list = os.listdir(upload_dir)

    resumes = []
    for filename in file_list:
        file_path = os.path.join(settings.MEDIA_URL, 'resumes', str(request.user.id), filename)
        resumes.append({
            'filename': filename,
            'url': file_path
        })

    return render(request, 'resumes/list_resumes.html', {'resumes': resumes})



@login_required
def delete_resume(request, filename):
    user_dir = get_uploaded_resumes_dir(request.user.id)
    file_path = os.path.join(user_dir, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect('list_resumes')



@login_required
def match_result(request):
    # Reuse match result from session if stored, or show empty
    matched_resume = request.session.get('matched_resume', None)
    return render(request, 'resumes/match_result.html', {
        'matched_resume': matched_resume
    })
    
    
@login_required
def upload_page(request):
    return render(request, 'resumes/upload_page.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('dashboard') 
