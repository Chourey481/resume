# app/models/sbert_model.py
from sentence_transformers import SentenceTransformer, util

# Load the Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_sbert_similarity(cv_text, job_description):
    # Encode the texts to get their embeddings
    cv_embedding = model.encode(cv_text, convert_to_tensor=True)
    job_description_embedding = model.encode(job_description, convert_to_tensor=True)

    # Compute cosine similarity
    similarity = util.cos_sim(cv_embedding, job_description_embedding)
    
    return similarity.item()  # Return as a scalar value