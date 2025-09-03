from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify
import requests
import fitz  
import os

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
URL = "https://openrouter.ai/api/v1/chat/completions"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""   
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    pdf_file = request.files['pdf']
    pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], pdf_file.filename)
    pdf_file.save(pdf_path)
    pdf_text = extract_text(pdf_path)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data_1 = {
        "model": "meta-llama/llama-3-8b-instruct",  
        "messages": [
            {"role": "system", "content": "You are an AI assistant that generates quiz questions based on the provided text."},
            {"role": "user", "content": f"Generate 10 multiple choice quiz questions based on the following text:\n\n{pdf_text}"}
        ]
    }
    
    response_quiz = requests.post(URL, json=data_1, headers=headers)
    
    if response_quiz.status_code == 200:
        result_1 = response_quiz.json()
        quiz_questions = result_1["choices"][0]["message"]["content"]
    else:
        return jsonify({"error": "Failed to generate quiz questions"}), 500
    
    return jsonify({"quiz": quiz_questions})

if __name__ == '__main__':
    app.run(debug=True)