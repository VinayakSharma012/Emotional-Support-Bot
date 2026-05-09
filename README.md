# Mental Health Support Chatbot# Mental Health Support Chatbot# Mental Health Support Chatbot



A supportive chatbot with crisis detection, emotion analysis, and AI-powered responses.



## FeaturesA web-based chatbot providing supportive conversations with crisis detection and emotion-aware responses.A web-based chatbot providing supportive conversations with crisis detection and emotion-aware responses.



- **Crisis Detection**: Identifies crisis keywords and provides helpline resources

- **Emotion Analysis**: Detects sentiment (positive/negative/neutral/distressed)

- **AI Responses**: Hugging Face integration with rule-based fallback## Features## Features

- **Safety First**: Blocks medical advice and ensures supportive tone

- **Responsive UI**: Clean web interface



## Tech Stack- **Safety Check**: Detects crisis keywords before processing- **Safety Check**: Detects crisis keywords before processing



- **Frontend**: HTML5, CSS3, JavaScript- **Emotion Detection**: Analyzes sentiment (positive/negative/neutral/distressed)- **Emotion Detection**: Analyzes sentiment (positive/negative/neutral/distressed)

- **Backend**: Python Flask

- **Emotion Detection**: TextBlob- **AI Responses**: OpenAI integration with rule-based fallback- **AI Responses**: OpenAI integration with rule-based fallback

- **AI**: Hugging Face gpt2 model (free)

- **Crisis Support**: Immediate helpline numbers when needed- **Crisis Support**: Immediate helpline numbers when needed

## Project Structure

- **Clean UI**: Responsive design with real-time emotion badge- **Clean UI**: Responsive design with real-time emotion badge

```

SupportBot/

├── backend/           # Python logic

│   ├── app.py        # Flask routes## Tech Stack## Tech Stack

│   ├── chat_handler.py

│   ├── emotion.py    # TextBlob sentiment

│   ├── safety.py     # Crisis detection

│   ├── responses.py  # Fallback responses- **Frontend**: HTML5, CSS3, Vanilla JavaScript- **Frontend**: HTML5, CSS3, Vanilla JavaScript

│   └── sanitizer.py  # Reply validation

├── config/- **Backend**: Python Flask- **Backend**: Python Flask

│   └── config.py     # Settings

├── frontend/         # Web UI- **Sentiment Analysis**: TextBlob- **Sentiment Analysis**: TextBlob

│   ├── index.html

│   ├── style.css- **AI**: OpenAI API (optional, has fallback)- **AI**: OpenAI API (optional, has fallback)

│   └── script.js

├── requirements.txt

├── run.sh            # Start script

└── .env              # API keys## Project Structure## Project Structure

```



## Setup

``````

1. **Create virtual environment**:

   ```bashSupportBot/SupportBot/

   python3 -m venv venv

   source venv/bin/activate├── backend/                 # Python backend├── backend/                 # Python backend

   ```

│   ├── app.py              # Flask routes│   ├── app.py              # Flask routes

2. **Install dependencies**:

   ```bash│   ├── chat_handler.py     # Message pipeline│   ├── chat_handler.py     # Message pipeline

   pip install -r requirements.txt

   python -m textblob.download_corpora│   ├── emotion.py          # Sentiment analysis│   ├── emotion.py          # Sentiment analysis

   ```

│   ├── safety.py           # Crisis detection│   ├── safety.py           # Crisis detection

3. **Add API key (optional)**:

   - Get token: https://huggingface.co/settings/tokens│   ├── responses.py        # Fallback templates│   ├── responses.py        # Fallback templates

   - Create `.env`:

     ```│   └── sanitizer.py        # Reply validation│   └── sanitizer.py        # Reply validation

     HUGGINGFACE_API_KEY=hf_your_token

     ```││



4. **Run**:├── config/                 # Configuration├── config/                 # Configuration

   ```bash

   ./run.sh│   └── config.py           # All settings│   └── config.py           # All settings

   ```

   Open: http://localhost:5000││



## How It Works├── frontend/               # Web UI├── frontend/               # Web UI



1. Safety check for crisis keywords│   ├── index.html│   ├── index.html

2. Emotion detection via TextBlob

3. AI response (Hugging Face) or rule-based fallback│   ├── style.css│   ├── style.css

4. Sanitization (blocks harmful content)

5. Response to user│   └── script.js│   └── script.js



## API Endpoints││



- `GET /` - Serve UI├── requirements.txt        # Python dependencies├── requirements.txt        # Python dependencies

- `GET /health` - Health check

- `POST /chat` - Send message├── run.sh                  # Start script├── run.sh                  # Start script



**Request**:└── .env                    # API keys (create this)└── .env                    # API keys (create this)

```json

{"message": "I'm feeling down"}``````

```



**Response**:

```json## Quick Start## Overview

{

  "reply": "Your supportive response...",

  "emotion": "negative",

  "is_crisis": false,### 1. SetupThis chatbot provides a safe space for students to talk about their feelings. It uses:

  "timestamp": "14:30"

}- **Safety checks** to detect crisis keywords before any processing

```

```bash- **Emotion detection** using TextBlob sentiment analysis

## Crisis Resources

python3 -m venv venv- **AI responses** via OpenAI API (with rule-based fallback)

- **iCall (India)**: 9152987821

- **Vandrevala Foundation**: 1860-2662-345source venv/bin/activate- **Supportive messaging** that never gives medical advice


pip install -r requirements.txt

python -m textblob.download_corpora## Tech Stack

```

- **Frontend**: HTML5, CSS3, Vanilla JavaScript

### 2. Configure (Optional)- **Backend**: Python Flask

- **Emotion Detection**: TextBlob (sentiment analysis)

Create `.env` file with your OpenAI API key:- **AI Generation**: OpenAI API (gpt-3.5-turbo) with fallback templates

```- **Environment**: python-dotenv for API key management

OPENAI_API_KEY=sk-your-key-here

```## Quick Start



**Note**: Works without API key using rule-based responses.### 1. Setup



### 3. Start Backend```bash

python3 -m venv venv

```bashsource venv/bin/activate

./run.shpip install -r requirements.txt

```python -m textblob.download_corpora

```

Backend runs on `http://localhost:5000`

### 2. Configure (Optional)

### 4. Open Frontend

Create `.env` file with your OpenAI API key:

Open `frontend/index.html` in your browser, or serve it:```

```bashOPENAI_API_KEY=sk-your-key-here

cd frontend```

python -m http.server 3000

```**Note**: Works without API key using rule-based responses.



Then open `http://localhost:3000`### 3. Start Backend



## API Endpoints```bash

./run.sh

| Method | Endpoint | Purpose |```

|--------|----------|---------|

| GET | `/` | Serve frontend |Backend runs on `http://localhost:5000`

| GET | `/health` | Health check |

| POST | `/chat` | Send message |### 4. Open Frontend



### POST /chatOpen `frontend/index.html` in your browser, or serve it:

```bash

**Request**:cd frontend

```jsonpython -m http.server 3000

{"message": "I'm feeling down"}```

```

Then open `http://localhost:3000`

**Response**:

```json## API Endpoints

{

  "reply": "It sounds like things have been tough...",| Method | Endpoint | Purpose |

  "emotion": "negative",|--------|----------|---------|

  "is_crisis": false,| GET | `/` | Serve frontend |

  "timestamp": "14:30"| GET | `/health` | Health check |

}| POST | `/chat` | Send message |

```

### POST /chat

## How It Works

**Request**:

``````json

User Message{"message": "I'm feeling down"}

    ↓```

[Safety Check] → Crisis? → Return crisis response

    ↓ No**Response**:

[Emotion Detection] → Classify sentiment```json

    ↓{

[AI Response] → OpenAI (or fallback)  "reply": "It sounds like things have been tough...",

    ↓  "emotion": "negative",

[Sanitize] → Block unsafe content  "is_crisis": false,

    ↓  "timestamp": "14:30"

Return to Frontend}

``````



## Crisis Keywords## How It Works



The chatbot detects these keywords and responds with helpline numbers:```

- suicide, kill myself, end my life, want to dieUser Message

- self harm, self-harm, cut myself, overdose    ↓

- no reason to live, hopeless, worthless, can't go on[Safety Check] → Crisis? → Return crisis response

    ↓ No

## Testing[Emotion Detection] → Classify sentiment

    ↓

```bash[AI Response] → OpenAI (or fallback)

# Test with crisis keyword    ↓

curl -X POST http://localhost:5000/chat \[Sanitize] → Block unsafe content

  -H "Content-Type: application/json" \    ↓

  -d '{"message": "I want to die"}'Return to Frontend

```

# Test normal message

curl -X POST http://localhost:5000/chat \## Crisis Keywords

  -H "Content-Type: application/json" \

  -d '{"message": "I feel good today"}'The chatbot detects these keywords and responds with helpline numbers:

```- suicide, kill myself, end my life, want to die

- self harm, self-harm, cut myself, overdose

## Troubleshooting- no reason to live, hopeless, worthless, can't go on



**Port 5000 in use?****Crisis Response**: Shows helpline numbers and encourages immediate contact

```bash

lsof -i :5000 && kill -9 <PID>### Emotion Labels

```

- **Positive** (polarity > 0.2): Happy, content, good news

**TextBlob error?**- **Negative** (polarity < -0.1): Sad, frustrated, concerned

```bash- **Neutral** (-0.1 ≤ polarity ≤ 0.2): Balanced, factual

python -m textblob.download_corpora- **Distressed** (negative + high subjectivity): Severe emotional distress

```

### AI Response Shaping

**CORS errors?**

- Ensure backend is running on `localhost:5000`The system prompt sent to OpenAI includes the detected emotion:

- Check `flask-cors` is installed

```

**OpenAI API issues?**"The user is feeling {emotion}. Your role is to listen, validate 

- App falls back to rule-based responses automaticallytheir feelings, and offer gentle support. Do NOT give medical 

- Check `.env` file has correct API keydiagnoses or advice."

```

## License

This ensures responses are contextually appropriate.

Educational project for college internship.

## Features

### Frontend
- ✅ Clean, calm UI with navy and teal color palette
- ✅ Real-time message display with timestamps
- ✅ Typing indicator (animated dots)
- ✅ Emotion badge with live updates
- ✅ Auto-growing textarea
- ✅ Responsive design (mobile-friendly)
- ✅ Crisis message styling (red border, alert color)
- ✅ Sidebar with helpline numbers always visible

### Backend
- ✅ Safety check runs BEFORE any processing
- ✅ Graceful fallback when API is unavailable
- ✅ Error handling with user-friendly messages
- ✅ CORS enabled for frontend communication
- ✅ Health check endpoint (`/health`)
- ✅ Timestamps on all responses
- ✅ No data storage (privacy by default)

### Safety & Ethics
- ✅ Never gives medical advice or diagnoses
- ✅ Blocks medication suggestions
- ✅ Recommends professional help when distressed
- ✅ Shows helpline numbers on crisis detection
- ✅ All responses encourage human connection

## API Endpoints

### GET `/`
Serves the `index.html` file.

### GET `/health`
Health check endpoint.
```json
{"status": "ok"}
```

### POST `/chat`
Main chat endpoint.

**Request**:
```json
{"message": "I've been feeling really down lately"}
```

**Response**:
```json
{
  "reply": "It sounds like things have been tough lately...",
  "emotion": "negative",
  "is_crisis": false,
  "timestamp": "14:30"
}
```

## Testing Checklist (for Professor Review)

✅ **Safety Check**: Message with "suicide" triggers crisis response  
✅ **Emotion Detection**: Sad message gets "negative" label  
✅ **Emotion Badge**: Updates in real-time as you chat  
✅ **AI Shaping**: Response matches the emotion context  
✅ **Fallback**: Comment out OPENAI_API_KEY in `.env`, chat still works  
✅ **Crisis Styling**: Red border and color on crisis messages  
✅ **Helplines**: Visible in sidebar always, in crisis response too  
✅ **Privacy**: No messages stored (check browser console/network)  
✅ **Clean Code**: Well-commented, readable, no console errors  

## Optional Features (Bonus)

You can add these if time allows:

1. **Quick mood buttons** at start of conversation
2. **Emotion history** tracking last 5 emotions
3. **Dark mode toggle** in sidebar
4. **Export chat** as `.txt` file

## Troubleshooting

### Port 5000 Already in Use
```bash
lsof -i :5000  # Find process
kill -9 <PID>  # Kill it
```

### TextBlob Not Working
```bash
python -m textblob.download_corpora
```

### CORS Errors in Frontend
- Make sure `flask_cors` is installed
- Check `CORS(app)` is in `app.py`
- Backend should be on `localhost:5000`

### OpenAI API Not Working
- Verify key is in `.env` file
- Check the key format (starts with `sk-`)
- App should fall back to rule-based responses automatically

## Key Implementation Details

### Why Rule-Based Fallback?
The app doesn't crash if OpenAI is unavailable. It gracefully falls back to contextually appropriate template responses based on detected emotion.

### Why Safety Check First?
Crisis situations need immediate, consistent responses. This isn't AI-generated—it's a guaranteed, vetted response with helpline numbers.

### Why Emotion Detection?
Shapes the AI system prompt and ensures responses match the user's emotional state. Also drives the UI badge.

### Why No Data Storage?
Privacy by default. No database, no localStorage, no logging. Each conversation is ephemeral and private.

## Limitations & Scope

This chatbot is **NOT a replacement for professional mental health care**. It:
- Provides peer support only
- Cannot diagnose conditions
- Cannot prescribe treatment
- Is not a crisis hotline (but directs to one)

Always encourage users to speak with counselors or call helplines for serious concerns.

## License

This is a college internship project. Use for educational purposes only.

## Support

For questions or issues:
1. Check troubleshooting section above
2. Review console errors (F12 in browser)
3. Check backend logs (terminal where you ran `python app.py`)
