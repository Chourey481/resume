from flask import Flask, render_template, request, jsonify
from models.sbert_model import get_sbert_similarity
from utils.file_handler import extract_text_from_pdf
from utils.similarity import calculate_similarity, generate_suggestions
import PyPDF2
import spacy
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

app = Flask(__name__)

# Load spaCy model for keyword extraction
nlp = spacy.load("en_core_web_sm")

# Define the function to extract keywords
def extract_keywords(text, pos_tags=["NOUN", "PROPN"]):
    """
    Extract keywords from text based on specified part-of-speech tags and get AI analysis.
    """
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in pos_tags]
    
    # Filter out common words and get unique keywords
    unique_keywords = list(set(keywords))
    return unique_keywords

def get_ai_analysis(resume_text, job_description, missing_keywords):
    """
    Get AI-powered analysis and suggestions using Groq.
    """
    prompt = f"""Analyze this resume against the job description and provide specific, actionable feedback:
    
Job Description: {job_description}

Missing Keywords: {', '.join(missing_keywords)}

Provide 3-4 specific suggestions on:
1. How to incorporate the missing keywords naturally
2. Skills that should be highlighted more
3. Areas of improvement
4. Professional development recommendations

Format the response in clear, bulleted points."""

    try:
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return "AI analysis currently unavailable. Please try again later."

# Function to read and extract text from resume
def read_resume(file):
    if file.filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    else:
        try:
            return file.read().decode('utf-8')  # Try to read as UTF-8
        except UnicodeDecodeError:
            return file.read().decode('ISO-8859-1')  # Fallback to ISO-8859-1

@app.route("/", methods=["GET", "POST"])
def index():
    # Render the main page with form for uploading resume and job description
    return render_template("index.html")

@app.route("/results", methods=["POST"])
def results():
    # Process the uploaded resume and job description
    resume_file = request.files.get("resume")
    job_description_text = request.form.get("job_description")

    # Check if inputs are missing
    if not resume_file or not job_description_text:
        return render_template("index.html", error="Please upload a resume and provide a job description.")

    # Extract text from resume file
    resume_text = read_resume(resume_file)

    # Calculate similarity score using SBERT
    similarity_score = get_sbert_similarity(resume_text, job_description_text)
    similarity_score = round(similarity_score * 100, 2)  # Convert to percentage for display

    # Extract keywords from both resume and job description
    resume_keywords = extract_keywords(resume_text)
    job_description_keywords = extract_keywords(job_description_text)
    
    # Find missing and matching keywords
    missing_keywords = list(set(job_description_keywords) - set(resume_keywords))
    matching_keywords = list(set(resume_keywords) & set(job_description_keywords))

    # Get AI-powered analysis and suggestions
    ai_analysis = get_ai_analysis(resume_text, job_description_text, missing_keywords)

    # Render the results page with calculated data
    return render_template(
        "results.html",
        score=similarity_score,
        missing_keywords=missing_keywords,
        matching_keywords=matching_keywords,
        ai_analysis=ai_analysis
    )

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
