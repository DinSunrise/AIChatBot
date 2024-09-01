let ws;
const messagesContainer = document.getElementById('messages');
const messageInput = document.getElementById('messageText');
const sendButton = document.getElementById('sendButton');


let accumulatedMessage = "";

function connectWebSocket() {
    ws = new WebSocket(`ws://${window.location.host}/chat/ws`);

    ws.onopen = () => {
        console.log('WebSocket connected');
        updateUIState(true);
    };

    ws.onmessage = (event) => {
        accumulatedMessage += event.data;
    
        if (event.data.endsWith("\n")) {
            accumulatedMessage = accumulatedMessage.trim();
            if (accumulatedMessage) {
                appendMessage('ai', accumulatedMessage);
            }
            accumulatedMessage = "";
        }
    };

    ws.onclose = () => {
        console.log('WebSocket disconnected');
        updateUIState(false);
        setTimeout(connectWebSocket, 5000);
    };

    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        updateUIState(false);
    };
}

function appendMessage(sender, content) {
    const message = document.createElement('li');
    message.className = `message ${sender}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = parseMarkdown(content);
    
    message.appendChild(contentDiv);
    messagesContainer.appendChild(message);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function parseMarkdown(text) {
    //line breaks
    text = text.replace(/\n/g, '<br>');
    
    //headers
    text = text.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    text = text.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    
    //bold text
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    //italic text
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    return text;
}

function sendMessage(event) {
    event.preventDefault();
    const message = messageInput.value.trim();
    if (message && ws.readyState === WebSocket.OPEN) {
        ws.send(message);
        appendMessage('user', message);
        messageInput.value = '';
    }
}

function updateUIState(connected) {
    sendButton.disabled = !connected;
    messageInput.disabled = !connected;
    messageInput.placeholder = connected ? "Type your message..." : "Connecting...";
}

document.getElementById('chatForm').addEventListener('submit', sendMessage);

connectWebSocket();
