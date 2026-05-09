// Set window.SUPPORTBOT_BACKEND_URL before this script to connect a deployed Flask API.
// GitHub Pages hosts static files only, so the app falls back to local supportive replies.
const BACKEND_URL = window.SUPPORTBOT_BACKEND_URL || "";
const WELCOME_MSG = "Hi! I'm your Emotional Support Chatbot. I'm here to listen. How are you feeling today? You can share anything - this is a safe, private space.";
const CRISIS_REPLY = "I'm really sorry you're feeling this way. If you might hurt yourself or someone else, please contact emergency services now or reach out to a crisis helpline: iCall 9152987821, Vandrevala 1860-2662-345, or AASRA 9820466726. You deserve immediate support.";

const chatMessages = document.getElementById("chatMessages");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const emotionBadge = document.getElementById("emotionBadge");
const chatForm = document.getElementById("chatForm");
const quickActionBtns = document.querySelectorAll(".quick-action-btn");

const isMobile = navigator.maxTouchPoints > 0 || /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

document.addEventListener("DOMContentLoaded", () => {
    addBotMessage(WELCOME_MSG);
    userInput.focus();
    setupEventListeners();
    if (isMobile) {
        document.body.style.touchAction = "manipulation";
    }
});

function setupEventListeners() {
    chatForm.addEventListener("submit", (e) => {
        e.preventDefault();
        sendMessage();
    });

    userInput.addEventListener("keydown", (e) => {
        if (!isMobile && e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    userInput.addEventListener("input", () => {
        resizeTextarea();
    });

    quickActionBtns.forEach((btn) => {
        btn.addEventListener("click", () => {
            const action = btn.getAttribute("data-action");
            userInput.value = action;
            resizeTextarea();
            sendMessage();
        });
    });
}

async function sendMessage() {
    const message = userInput.value.trim();

    if (!message) {
        return;
    }

    addUserMessage(message);
    userInput.value = "";
    resizeTextarea();

    sendBtn.disabled = true;
    sendBtn.classList.add("loading");

    showTypingIndicator();

    try {
        const data = BACKEND_URL
            ? await sendToBackend(message)
            : getStaticReply(message);

        hideTypingIndicator();

        if (data.is_crisis) {
            addCrisisMessage(data.reply, data.timestamp);
        } else {
            addBotMessage(data.reply, data.timestamp);
        }

        updateEmotionBadge(data.emotion);
    } catch (error) {
        console.error("Error:", error);
        hideTypingIndicator();
        const fallback = getStaticReply(message);
        addBotMessage(fallback.reply, fallback.timestamp);
        updateEmotionBadge(fallback.emotion);
    } finally {
        sendBtn.disabled = false;
        sendBtn.classList.remove("loading");
        userInput.focus();
    }
}

async function sendToBackend(message) {
    const response = await fetch(BACKEND_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: message }),
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
}

function getStaticReply(message) {
    const text = message.toLowerCase();
    const emotion = detectStaticEmotion(text);
    const timestamp = new Date().toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
    });

    if (isCrisisMessage(text)) {
        return {
            reply: CRISIS_REPLY,
            emotion: "distressed",
            is_crisis: true,
            timestamp,
        };
    }

    const replies = {
        positive: "I'm glad there is some light in your day. What do you think helped you feel this way?",
        negative: "That sounds heavy. I'm here with you. What has been the hardest part to carry today?",
        distressed: "That sounds really intense. Try taking one slow breath with me, then tell me what feels most urgent right now.",
        neutral: "Thanks for sharing that. What's been on your mind the most today?",
    };

    return {
        reply: replies[emotion],
        emotion,
        is_crisis: false,
        timestamp,
    };
}

function detectStaticEmotion(text) {
    const distressedWords = ["panic", "overwhelmed", "scared", "terrified", "desperate", "hopeless"];
    const negativeWords = ["sad", "low", "depressed", "anxious", "stress", "stressed", "lonely", "tired", "angry", "upset"];
    const positiveWords = ["good", "okay", "fine", "happy", "better", "calm", "grateful", "hopeful"];

    if (distressedWords.some((word) => text.includes(word))) {
        return "distressed";
    }

    if (negativeWords.some((word) => text.includes(word))) {
        return "negative";
    }

    if (positiveWords.some((word) => text.includes(word))) {
        return "positive";
    }

    return "neutral";
}

function isCrisisMessage(text) {
    const crisisPhrases = [
        "kill myself",
        "end my life",
        "suicide",
        "self harm",
        "hurt myself",
        "can't go on",
        "cant go on",
    ];

    return crisisPhrases.some((phrase) => text.includes(phrase));
}

function addUserMessage(message, timestamp = null) {
    const messageDiv = document.createElement("div");
    messageDiv.className = "message user-message";

    if (!timestamp) {
        timestamp = new Date().toLocaleTimeString("en-US", {
            hour: "2-digit",
            minute: "2-digit",
            hour12: false,
        });
    }

    messageDiv.innerHTML = `
        ${escapeHtml(message)}
        <span class="message-timestamp">${timestamp}</span>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollIntoView({ behavior: "smooth", block: "end" });
}

function addBotMessage(message, timestamp = null) {
    const messageDiv = document.createElement("div");
    messageDiv.className = "message bot-message";

    if (!timestamp) {
        timestamp = new Date().toLocaleTimeString("en-US", {
            hour: "2-digit",
            minute: "2-digit",
            hour12: false,
        });
    }

    messageDiv.innerHTML = `
        ${escapeHtml(message)}
        <span class="message-timestamp">${timestamp}</span>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollIntoView({ behavior: "smooth", block: "end" });
}

function addCrisisMessage(message, timestamp = null) {
    const messageDiv = document.createElement("div");
    messageDiv.className = "message bot-message crisis-message";

    if (!timestamp) {
        timestamp = new Date().toLocaleTimeString("en-US", {
            hour: "2-digit",
            minute: "2-digit",
            hour12: false,
        });
    }

    messageDiv.innerHTML = `
        ${escapeHtml(message)}
        <span class="message-timestamp">${timestamp}</span>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollIntoView({ behavior: "smooth", block: "end" });
}

function showTypingIndicator() {
    const typingDiv = document.createElement("div");
    typingDiv.id = "typingIndicator";
    typingDiv.className = "message bot-message typing";

    typingDiv.innerHTML = `
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
    `;

    chatMessages.appendChild(typingDiv);
    chatMessages.scrollIntoView({ behavior: "smooth", block: "end" });
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById("typingIndicator");
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

function updateEmotionBadge(emotion) {
    const emotionText = emotion.charAt(0).toUpperCase() + emotion.slice(1);
    emotionBadge.textContent = `Feeling: ${emotionText}`;
    emotionBadge.classList.remove("positive", "negative", "neutral", "distressed");
    emotionBadge.classList.add(emotion);
}

function resizeTextarea() {
    userInput.style.height = "auto";
    userInput.style.height = Math.min(userInput.scrollHeight, 120) + "px";
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}
