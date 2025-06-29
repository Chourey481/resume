# app/utils/similarity.py
from .text_processing import preprocess_text
from models.sbert_model import get_sbert_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume_text, job_description, method='tfidf'):
    resume_text = preprocess_text(resume_text)
    job_description = preprocess_text(job_description)
    output =get_sbert_similarity(resume_text, job_description)
    return round(output,2)

def generate_suggestions(similarity_score):
    suggestions = []
    
    if similarity_score < 0.5:
        suggestions.append("Add more relevant experience.")
        suggestions.append("Use keywords from the job description.")
    elif similarity_score < 0.75:
        suggestions.append("Include specific skills required for the job.")
    elif similarity_score < 0.9:
        suggestions.append("Tailor your resume summary.")
    
    return suggestions    
