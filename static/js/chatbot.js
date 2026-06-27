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

function parseMarkdown(text) {
    if (!text) return "";
    
    // Escaping HTML characters first to avoid XSS
    let escaped = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
        
    // Split by newlines to parse blocks
    const lines = escaped.split('\n');
    let inList = false;
    let result = [];
    
    for (let i = 0; i < lines.length; i++) {
        let line = lines[i];
        let trimmed = line.trim();
        
        // Handle bold: **text** -> <strong>text</strong>
        line = line.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
        // Handle italic: *text* -> <em>text</em>
        line = line.replace(/\*(.*?)\*/g, "<em>$1</em>");
        
        // Check for headers
        if (trimmed.startsWith('### ')) {
            if (inList) { result.push('</ul>'); inList = false; }
            result.push(`<h4 style="margin: 0.8rem 0 0.4rem 0; font-weight: bold; font-size: 1.1rem; color: #1a1a1a;">${trimmed.substring(4)}</h4>`);
        } else if (trimmed.startsWith('## ')) {
            if (inList) { result.push('</ul>'); inList = false; }
            result.push(`<h3 style="margin: 1rem 0 0.5rem 0; font-weight: bold; font-size: 1.25rem; color: #1a1a1a;">${trimmed.substring(3)}</h3>`);
        } else if (trimmed.startsWith('# ')) {
            if (inList) { result.push('</ul>'); inList = false; }
            result.push(`<h2 style="margin: 1.2rem 0 0.6rem 0; font-weight: bold; font-size: 1.4rem; color: #1a1a1a;">${trimmed.substring(2)}</h2>`);
        }
        // Check for bullet list item: starts with "* " or "- "
        else if (trimmed.startsWith('* ') || trimmed.startsWith('- ') || trimmed.startsWith('• ')) {
            if (!inList) {
                result.push('<ul style="margin: 0.5rem 0; padding-left: 1.5rem; list-style-type: disc;">');
                inList = true;
            }
            // Remove bullet prefix
            let content = line.trim().replace(/^[\*\-\u2022]\s+/, "");
            result.push(`<li style="margin-bottom: 0.25rem; line-height: 1.5;">${content}</li>`);
        } 
        // Regular line
        else {
            if (inList) {
                result.push('</ul>');
                inList = false;
            }
            
            if (trimmed === '') {
                result.push('<br>');
            } else {
                result.push(`<p style="margin: 0 0 0.5rem 0; line-height: 1.5;">${line}</p>`);
            }
        }
    }
    
    if (inList) {
        result.push('</ul>');
    }
    
    return result.join('\n');
}

function addMessage(text, isUser) {
    const container = document.getElementById('chatMessages');
    const welcome = document.getElementById('chatWelcome');
    if (welcome) welcome.style.display = 'none';

    const msg = document.createElement('div');
    msg.className = 'message ' + (isUser ? 'user-message' : 'bot-message');
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    
    if (isUser) {
        bubble.textContent = text;
    } else {
        bubble.innerHTML = parseMarkdown(text);
    }
    
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
