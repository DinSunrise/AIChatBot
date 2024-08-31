var ws = new WebSocket("ws://0.0.0.0:8000/chat/ws");

ws.onmessage = function(event) {
    var messages = document.getElementById('messages');
    var message = document.createElement('li');
    
    var content = document.createElement('div');
    content.textContent = event.data;
    content.className = "message-content"; 

    message.appendChild(content);

    if (event.data.startsWith("AI:")) {
        message.className = "ai-message";
    } else {
        message.className = "user-message";
    }

    messages.appendChild(message);
};

function sendMessage(event) {
    var input = document.getElementById("messageText");
    var userMessage = input.value; 

    ws.send(userMessage);

    var messages = document.getElementById('messages');
    var message = document.createElement('li');
    
    var content = document.createElement('div');
    content.textContent = userMessage; 

    message.appendChild(content);
    message.className = "user-message";
    messages.appendChild(message);
    input.value = '';
    event.preventDefault();
}
