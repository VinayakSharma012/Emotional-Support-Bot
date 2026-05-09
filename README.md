# Emotional Support Bot

A web-based emotional support chatbot with crisis keyword detection, emotion-aware responses, and a responsive chat interface.

Live site: https://vinayaksharma012.github.io/Emotional-Support-Bot/

Repository: https://github.com/VinayakSharma012/Emotional-Support-Bot

## Features

- Crisis keyword detection with immediate helpline guidance
- Emotion detection for positive, negative, neutral, and distressed messages
- Supportive chatbot responses with a rule-based fallback
- Responsive HTML, CSS, and JavaScript interface
- Flask backend for local API-powered chat
- GitHub Pages deployment for the static frontend

## Tech Stack

- Frontend: HTML5, CSS3, vanilla JavaScript
- Backend: Python Flask
- Sentiment analysis: TextBlob
- Deployment: GitHub Pages

## Project Structure

```text
SupportBot/
├── .github/workflows/      # GitHub Pages deployment workflow
├── backend/                # Flask backend and chat pipeline
├── config/                 # App configuration
├── docs/                   # Static site published to GitHub Pages
├── frontend/               # Local frontend served by Flask
├── requirements.txt        # Python dependencies
└── README.md
```

## Local Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
python -m textblob.download_corpora
```

Run the Flask backend:

```bash
python backend/app.py
```

Open the local app at:

```text
http://localhost:5000
```

## API

Health check:

```text
GET /health
```

Send a chat message:

```text
POST /chat
```

Example request:

```json
{
  "message": "I'm feeling stressed"
}
```

Example response:

```json
{
  "reply": "Your supportive response...",
  "emotion": "negative",
  "is_crisis": false,
  "timestamp": "14:30"
}
```

## GitHub Pages

The live GitHub Pages site is served from the `gh-pages` branch:

https://vinayaksharma012.github.io/Emotional-Support-Bot/

The `docs/` folder contains the static version of the app. Because GitHub Pages cannot run Flask, the hosted site uses static fallback responses unless a deployed backend URL is configured in `docs/script.js`.

## Crisis Resources

- iCall: 9152987821
- Vandrevala Foundation: 1860-2662-345
- AASRA: 9820466726

This project is for peer-style support only. It is not a replacement for therapy, medical care, emergency services, or professional mental health support.
