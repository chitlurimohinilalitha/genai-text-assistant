# GenAI Text Assistant

A Flask-based web application that uses Generative AI to summarize text,
answer questions from user-provided context, and hold conversational chats.

## Overview
This project demonstrates practical applications of Generative AI (Large Language
Models) integrated into a Python web app. It showcases three core GenAI use cases:
text summarization, context-based question answering, and conversational chat.

## Features
- Text Summarization - condenses long passages into a configurable number of sentences
- Question Answering - answers questions based on a given context passage
- Chat Assistant - maintains conversation history for multi-turn chat
- Simple REST API (Flask) with JSON request/response
- Environment-variable based API key configuration (secure, no hardcoded keys)

## Tech Stack
- Language: Python
- Web Framework: Flask
- Generative AI: LLM API integration (chat completions endpoint)
- HTTP Client: requests

## Project Structure
main.py - Flask app + GenAI integration functions
templates/index.html - Simple front-end for summarization/chat/QA
README.md

## API Endpoints
/summarize (POST) - Summarizes input text into N sentences
/qa (POST) - Answers a question based on given context
/chat (POST) - Multi-turn conversational chat

## Setup and Running
pip install -r requirements.txt
export GENAI_API_KEY="your_api_key_here"
python main.py

Then open http://127.0.0.1:5000/ in your browser.

## How It Works
1. User submits text/question/message through the web interface
2. Flask routes the request to the appropriate GenAI helper function
3. The helper builds a prompt and sends it to the LLM API
4. The model's response is parsed and returned as JSON to the front-end
