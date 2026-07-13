import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
# Set your API key as an environment variable before running:
#   export GENAI_API_KEY="your_api_key_here"
API_KEY = os.environ.get("GENAI_API_KEY", "")
API_URL = "https://api.openai.com/v1/chat/completions"  # example endpoint


# ---------------------------------------------------------
# Core GenAI helper: sends a prompt and returns model response
# ---------------------------------------------------------
def query_genai(prompt, max_tokens=300, temperature=0.5):
    if not API_KEY:
        return "Error: GENAI_API_KEY not set. Please configure your API key."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        return f"Error calling GenAI API: {str(e)}"


# ---------------------------------------------------------
# Feature 1: Text Summarization
# ---------------------------------------------------------
def summarize_text(text, num_sentences=3):
    prompt = (
        f"Summarize the following text in {num_sentences} concise sentences:\n\n"
        f"{text}"
    )
    return query_genai(prompt, max_tokens=200)


# ---------------------------------------------------------
# Feature 2: Question Answering based on provided context
# ---------------------------------------------------------
def answer_question(context, question):
    prompt = (
        f"Based on the following context, answer the question clearly and concisely.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n"
        f"Answer:"
    )
    return query_genai(prompt, max_tokens=200)


# ---------------------------------------------------------
# Feature 3: Simple Chat Assistant
# ---------------------------------------------------------
def chat_response(user_message, conversation_history=None):
    if conversation_history is None:
        conversation_history = []

    messages = conversation_history + [{"role": "user", "content": user_message}]

    if not API_KEY:
        return "Error: GENAI_API_KEY not set."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": 300,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        return f"Error calling GenAI API: {str(e)}"


# ---------------------------------------------------------
# Flask Routes
# ---------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data.get('text', '')
    num_sentences = data.get('num_sentences', 3)

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    summary = summarize_text(text, num_sentences)
    return jsonify({'summary': summary})


@app.route('/qa', methods=['POST'])
def qa():
    data = request.get_json()
    context = data.get('context', '')
    question = data.get('question', '')

    if not context or not question:
        return jsonify({'error': 'Context and question are required'}), 400

    answer = answer_question(context, question)
    return jsonify({'answer': answer})


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    history = data.get('history', [])

    if not message:
        return jsonify({'error': 'No message provided'}), 400

    reply = chat_response(message, history)
    return jsonify({'reply': reply})


if __name__ == '__main__':
    app.run(debug=True)
