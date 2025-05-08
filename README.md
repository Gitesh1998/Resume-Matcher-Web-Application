# Resume-Matcher-Web-Application

A Django-based web application that allows users to **upload resumes** and **match them against job descriptions** using **TF-IDF vectorization** and **cosine similarity**. The system ranks all uploaded resumes and displays the **top 3 most relevant matches** for the given job description.

## 🚀 Features

- User signup and login with Django authentication
- Secure resume upload per user (PDF format)
- Job description input interface
- Intelligent resume matching using:
  - `TfidfVectorizer` from scikit-learn
  - Cosine similarity scoring
- Display of top 3 matched resumes with similarity percentages
- Resume list and deletion functionality
- Session-based match result handling

## 🛠️ Tech Stack

- **Backend:** Django 5.2
- **Frontend:** HTML/CSS via Django templates
- **Matching Engine:** scikit-learn (`TfidfVectorizer`, `cosine_similarity`)
- **PDF Parsing:** PyPDF2
- **Auth:** Django `UserCreationForm`, login-required views
