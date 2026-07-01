# Prompt for Claude: Generate Project Report

Use this prompt in Claude to generate a formal project report for this repository.

---

Write a detailed academic or portfolio project report for **Emotional Support Chatbot**.

## Project Overview

This project is a local web-based emotional support chatbot for students. It provides a chat interface where users can share how they feel. The system detects emotional tone, checks for crisis-related messages, optionally uses the Groq API for AI-generated empathetic replies, and falls back to predefined supportive responses when AI is unavailable.

Important: this chatbot is for peer support only. It is not a replacement for therapy, medical treatment, emergency services, licensed counselors, or psychiatrists.

## Features

- Crisis keyword detection with helpline guidance.
- Emotion detection using TextBlob sentiment analysis.
- AI replies through Groq when `GROQ_API_KEY` is configured.
- Fallback responses when Groq is unavailable.
- Response sanitization to avoid diagnosis, prescription, or unsafe medical advice.
- Recent conversation history included in AI prompts.
- Flask backend with `/chat` and `/health` endpoints.
- Vanilla HTML, CSS, and JavaScript frontend.
- Responsive dark theme UI.
- Local `.env` configuration for private API keys.

## Technology Stack

- Frontend: HTML5, CSS3, Vanilla JavaScript
- Backend: Python Flask
- CORS: Flask-CORS
- Sentiment analysis: TextBlob
- Environment variables: python-dotenv
- HTTP client: requests
- Optional AI API: Groq API
- Default port: 8000

## Project Structure

```text
SupportBot/
├── backend/
│   ├── app.py
│   ├── chat_handler.py
│   ├── emotion.py
│   ├── safety.py
│   ├── responses.py
│   └── sanitizer.py
├── config/
│   └── config.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── .env.example
├── requirements.txt
└── README.md
```

## Workflow

1. User submits a message from the frontend.
2. Flask receives it through `POST /chat`.
3. The backend validates and cleans recent conversation history.
4. `detect_emotion()` classifies the message as positive, neutral, negative, or distressed.
5. `get_ai_response()` sends the prompt to Groq if `GROQ_API_KEY` is configured.
6. If Groq responds, `detect_crisis_intent()` performs an additional AI crisis check.
7. Crisis responses override normal AI replies.
8. If Groq is unavailable, keyword safety detection runs.
9. If no crisis is detected, a fallback supportive response is used.
10. The reply is sanitized and returned to the frontend with emotion, crisis flag, and timestamp.

## Groq API Details

Endpoint:

```text
https://api.groq.com/openai/v1/chat/completions
```

Environment variables:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_FALLBACK_MODELS=llama-3.3-70b-versatile
```

Do not include real API keys in the report.

## Safety Design

Explain both safety layers:

- Keyword crisis detection in `backend/safety.py`.
- AI crisis intent detection through Groq when an AI response is available.

The crisis response includes Indian helplines:

- iCall India: 9152987821
- Vandrevala Foundation: 1860-2662-345
- AASRA: 9820466726

## Suggested Report Sections

1. Title Page
2. Abstract
3. Introduction
4. Problem Statement
5. Objectives
6. Scope
7. Technology Stack
8. System Architecture
9. Module Description
10. Message Processing Workflow
11. Safety and Ethical Considerations
12. User Interface Design
13. Implementation Details
14. Testing and Validation
15. Limitations
16. Future Enhancements
17. Conclusion
18. References

## Testing Notes

Mention these checks:

- Python files compiled successfully.
- JavaScript syntax check passed.
- `/health` endpoint tested.
- `/chat` fallback path tested.
- Real Groq request tested successfully.
- Sensitive `.env` file is ignored by Git.

## Limitations

- TextBlob emotion detection is simple and may miss nuance.
- Keyword crisis detection can have false positives or false negatives.
- AI output depends on Groq API availability and key limits.
- No database, user accounts, or persistent conversation storage.
- The app is not clinically validated and must not be described as medical software.

## Future Enhancements

- Stronger emotion classification model.
- More robust safety classifier.
- Multilingual support.
- Session persistence with privacy controls.
- User feedback buttons.
- Automated tests.
- Deployment guide.
- Accessibility improvements.

Now generate the full report in a formal, clear style. Use tables where helpful and include a simple text architecture diagram.
