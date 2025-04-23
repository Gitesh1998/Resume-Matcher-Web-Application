import os
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(filepath):
    with open(filepath, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''.join([page.extract_text() or '' for page in reader.pages])
    return text

def match_resume_to_job(job_desc, resumes_dir):
    resumes = []
    filenames = []

    for filename in os.listdir(resumes_dir):
        if filename.endswith('.pdf'):
            path = os.path.join(resumes_dir, filename)
            text = extract_text_from_pdf(path)
            resumes.append(text)
            filenames.append(filename)

    if not resumes:
        return None

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform([job_desc] + resumes)
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]

    best_idx = similarity_scores.argmax()
    best_match = {
        'filename': filenames[best_idx],
        'similarity': round(similarity_scores[best_idx] * 100, 2),
        'download_url': f"/media/resumes/{filenames[best_idx]}"
    }
    return best_match
