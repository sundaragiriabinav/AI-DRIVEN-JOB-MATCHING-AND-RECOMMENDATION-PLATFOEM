from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

app = Flask(__name__)

def clean_text(text):
    """Basic NLP preprocessing: remove special chars and lowercase."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def calculate_match(resume, job_desc):
    # 1. Clean data
    resume = clean_text(resume)
    job_desc = clean_text(job_desc)
    
    # 2. Vectorize text (Convert words to numbers)
    content = [resume, job_desc]
    vectorizer = TfidfVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(content)
    
    # 3. Calculate Cosine Similarity
    # This measures the 'angle' between the two text vectors
    similarity_matrix = cosine_similarity(matrix)
    score = round(similarity_matrix[0][1] * 100, 2)
    return score

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    resume_text = data.get('resume', '')
    job_text = data.get('job', '')
    
    if not resume_text or not job_text:
        return jsonify({'error': 'Missing input'}), 400
    
    match_score = calculate_match(resume_text, job_text)
    return jsonify({'score': match_score})

if __name__ == '__main__':
    app.run(debug=True)