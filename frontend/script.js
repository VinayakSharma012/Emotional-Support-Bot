const BACKEND_URL = "/chat";
const WELCOME_MSG = "Hi! I'm your Emotional Support Chatbot. I'm here to listen. How are you feeling today? You can share anything - this is a safe, private space.";

const chatMessages = document.getElementById("chatMessages");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const emotionBadge = document.getElementById("emotionBadge");
const chatForm = document.getElementById("chatForm");
const conversationHistory = [];

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
}

async function sendMessage() {
    const message = userInput.value.trim();

    if (!message) {
        return;
    }

    const history = getRecentHistory();
    addUserMessage(message);
    userInput.value = "";
    resizeTextarea();

    sendBtn.disabled = true;
    sendBtn.classList.add("loading");

    showTypingIndicator();

    try {
        const response = await fetch(BACKEND_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: message, history: history }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        hideTypingIndicator();

        if (data.is_crisis) {
            addCrisisMessage(data.reply, data.timestamp);
        } else {
            addBotMessage(data.reply, data.timestamp);
        }

        rememberConversation(message, data.reply);
        updateEmotionBadge(data.emotion);
    } catch (error) {
        console.error("Error:", error);
        hideTypingIndicator();
        addBotMessage(
            "Sorry, I couldn't connect. Please check the server and try again."
        );
    } finally {
        sendBtn.disabled = false;
        sendBtn.classList.remove("loading");
        userInput.focus();
    }
}

function getRecentHistory() {
    return conversationHistory.slice(-8);
}

function rememberConversation(userMessage, botReply) {
    conversationHistory.push({ role: "user", content: userMessage });
    conversationHistory.push({ role: "bot", content: botReply });

    if (conversationHistory.length > 16) {
        conversationHistory.splice(0, conversationHistory.length - 16);
    }
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
