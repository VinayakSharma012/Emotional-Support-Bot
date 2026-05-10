# Emotional Support Chatbot

A professional mental health support chatbot for students with crisis detection, emotion analysis, and empathetic responses.

## Features

✅ **Crisis Detection** - Identifies crisis keywords and provides immediate helpline guidance  
✅ **Emotion Analysis** - Detects emotional states (positive, negative, neutral, distressed)  
✅ **Context-Aware Responses** - Tailored replies for specific topics (crushes, exams, anxiety, etc.)  
✅ **AI-Powered Replies** - Hugging Face integration for intelligent responses (optional)  
✅ **Fallback Responses** - Safe, empathetic default messages when AI is unavailable  
✅ **Dark Theme UI** - Professional, modern, mobile-responsive interface  
✅ **Local & Private** - Run locally for complete privacy and control  

## Tech Stack

- **Frontend:** HTML5, CSS3, Vanilla JavaScript (no frameworks)
- **Backend:** Python Flask
- **Sentiment Analysis:** TextBlob
- **AI Responses:** Hugging Face Inference API (optional)
- **Port:** 8000 (configurable)

## Project Structure

```
SupportBot/
├── backend/                # Flask app & chat pipeline
│   ├── app.py             # Main Flask application
│   ├── chat_handler.py    # Message processing pipeline
│   ├── emotion.py         # Emotion detection
│   ├── safety.py          # Crisis keyword detection
│   ├── responses.py       # Response generation
│   └── sanitizer.py       # Reply validation
├── frontend/               # Web interface
│   ├── index.html         # Chat UI
│   ├── script.js          # Frontend logic
│   └── style.css          # Dark theme styles
├── config/                # Configuration
│   └── config.py          # Settings & constants
├── .env.example           # Environment template
├── requirements.txt       # Python dependencies
└── README.md
```

## Quick Start

### 1. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

```bash
pip install -r requirements.txt
python -m textblob.download_corpora
```

### 2. Configure (Optional)

For AI responses from Hugging Face:

```bash
cp .env.example .env
```

Edit `.env` and add your Hugging Face API key:

```env
HUGGINGFACE_API_KEY=your_api_key_here
HUGGINGFACE_MODEL=HuggingFaceH4/zephyr-7b-beta
```

**Note:** Keep `.env` private. It's in `.gitignore`.

### 3. Run the Bot

```bash
python backend/app.py
```

The app will be available at:

```
http://localhost:8000
```

## API Endpoints

### Health Check

```
GET /health
```

**Response:**
```json
{
  "status": "ok"
}
```

### Send Message

```
POST /chat
Content-Type: application/json
```

**Request:**
```json
{
  "message": "I'm feeling stressed about exams",
  "history": [
    {"role": "user", "content": "Hi"},
    {"role": "bot", "content": "Hello! How can I help?"}
  ]
}
```

**Response:**
{
  "reply": "Academic pressure can be really heavy. What's the thing about school or exams that's causing the most stress?",
  "emotion": "negative",
  "is_crisis": false,
  "timestamp": "14:30"
}
```

## Message Processing Pipeline

The chatbot processes messages in this order:

1. **Safety Check** → Detects crisis keywords, returns helpline info if needed
2. **Emotion Detection** → Analyzes sentiment (positive/negative/neutral/distressed)
3. **Context-Aware Response** → Checks for specific topics (exams, relationships, anxiety, etc.)
4. **AI Response** → Uses Hugging Face if API key is configured
5. **Fallback Response** → Safe, supportive default message
6. **Sanitization** → Validates and formats the final reply

## Crisis Resources

If you or someone you know is in crisis, please reach out immediately:

- **iCall (India):** 9152987821
- **Vandrevala Foundation:** 1860-2662-345
- **AASRA:** 9820466726

## Disclaimer

⚠️ **This chatbot is for peer support only.** It is **NOT** a replacement for:
- Professional mental health therapy
- Medical treatment
- Emergency services
- Licensed counselors or psychiatrists

If you're experiencing a serious mental health crisis, please call emergency services or contact a mental health professional immediately.

## Configuration

All settings are in `config/config.py`:

```python
FLASK_PORT = 8000                    # Server port
FLASK_DEBUG = False                  # Debug mode
HUGGINGFACE_MODEL = "..."            # AI model to use
MAX_HISTORY_MESSAGES = 8             # Conversation context size
POLARITY_POSITIVE_THRESHOLD = 0.1    # Emotion detection threshold
```

## Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
HUGGINGFACE_API_KEY=your_key_here
FLASK_DEBUG=false
FLASK_PORT=8000
```

## Development

To modify responses or add new features:

- **Emotion detection:** `backend/emotion.py`
- **Crisis detection:** `backend/safety.py`
- **Fallback responses:** `backend/responses.py`
- **Message processing:** `backend/chat_handler.py`
- **Frontend UI:** `frontend/`

## License

This project is open source. Feel free to use, modify, and distribute.

## Support

For issues, feature requests, or contributions, please open a GitHub issue or submit a pull request.

---

**Made with ❤️ for student mental health and wellbeing.**
