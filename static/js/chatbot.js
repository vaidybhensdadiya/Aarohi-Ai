/**
 * Chatbot.js - WhatsApp-style chat UI for Aarohi AI
 * Loader, auto-scroll, API calls with JWT
 */

function getToken() {
    return localStorage.getItem('aarohi_token');
}

function getAPIHeaders() {
    const token = getToken();
    return {
        'Content-Type': 'application/json',
        'Authorization': token ? 'Bearer ' + token : ''
    };
}

function addMessage(text, isUser) {
    const container = document.getElementById('chatMessages');
    const welcome = document.getElementById('chatWelcome');
    if (welcome) welcome.style.display = 'none';

    const msg = document.createElement('div');
    msg.className = 'message ' + (isUser ? 'user-message' : 'bot-message');
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = text;
    msg.appendChild(bubble);
    container.appendChild(msg);
    scrollToBottom();
}

function addLoader() {
    const container = document.getElementById('chatMessages');
    const welcome = document.getElementById('chatWelcome');
    if (welcome) welcome.style.display = 'none';

    const tmpl = document.getElementById('loaderTemplate');
    const loader = tmpl.content.cloneNode(true);
    container.appendChild(loader);
    scrollToBottom();
}

function removeLoader() {
    const loader = document.querySelector('.loader-bubble');
    if (loader) loader.closest('.message').remove();
}

function scrollToBottom() {
    const container = document.getElementById('chatMessages');
    if (container) container.scrollTop = container.scrollHeight;
}

async function sendMessage(text) {
    if (!text.trim()) return;

    addMessage(text, true);
    addLoader();

    const input = document.getElementById('chatInput');
    const btn = document.getElementById('chatSendBtn');
    if (input) input.disabled = true;
    if (btn) btn.disabled = true;

    try {
        const res = await fetch('/api/chatbot/chat', {
            method: 'POST',
            headers: getAPIHeaders(),
            body: JSON.stringify({ message: text.trim() })
        });
        const data = await res.json();
        removeLoader();

        if (!res.ok) {
            addMessage(data.error || 'Something went wrong. Please try again.', false);
            return;
        }
        addMessage(data.response, false);
    } catch (err) {
        removeLoader();
        addMessage('Network error. Please try again.', false);
    } finally {
        if (input) {
            input.disabled = false;
            input.value = '';
            input.focus();
        }
        if (btn) btn.disabled = false;
    }
}

function initChatbot() {
    const form = document.getElementById('chatForm');
    const input = document.getElementById('chatInput');

    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const text = input ? input.value : '';
            sendMessage(text);
        });
    }

    if (input) input.focus();
}
