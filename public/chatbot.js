// Chatbot JavaScript

let conversationHistory = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('Chatbot page loaded');
    loadUserInfo();
    loadLocation();
    autoResizeTextarea();
});

// Load user info
function loadUserInfo() {
    const user = JSON.parse(localStorage.getItem('krishishakti_user') || sessionStorage.getItem('krishishakti_user') || '{}');
    const userName = user.name || 'User';
    document.getElementById('welcome-user').textContent = userName;
    
    // Set user avatar initial
    const initial = userName.charAt(0).toUpperCase();
    document.getElementById('user-initial').textContent = initial;
}

// Load location
function loadLocation() {
    const cached = localStorage.getItem('user_location');
    if (cached) {
        const location = JSON.parse(cached);
        document.getElementById('location-text').textContent = `${location.city}, ${location.country}`;
    } else {
        document.getElementById('location-text').textContent = 'Location unavailable';
    }
}

// Auto-resize textarea
function autoResizeTextarea() {
    const textarea = document.getElementById('chat-input');
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
}

// Handle Enter key
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Send quick message
function sendQuickMessage(message) {
    document.getElementById('chat-input').value = message;
    sendMessage();
}

// Send message
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    input.value = '';
    input.style.height = 'auto';
    
    // Disable send button
    const sendBtn = document.getElementById('send-btn');
    sendBtn.disabled = true;
    
    // Show typing indicator
    showTypingIndicator();
    
    // Update status
    updateStatus('loading', 'Thinking...');
    
    try {
        // Get sensor context
        const sensorData = await getSensorContext();
        
        // Send to backend
        const response = await fetch('/api/chatbot/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                sensorData: sensorData,
                history: conversationHistory.slice(-10) // Last 10 messages for context
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to get response');
        }
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        // Add bot response
        addMessage(data.response, 'bot');
        
        // Update conversation history
        conversationHistory.push(
            { role: 'user', content: message },
            { role: 'assistant', content: data.response }
        );
        
        // Update status
        updateStatus('ready', 'Ready');
        
    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator();
        addMessage('🌾 I\'m here to help! Ask me about watering, fertilizers, pests, diseases, soil, planting, harvesting, or any farming question.', 'bot');
        updateStatus('ready', 'Ready');
    }
    
    // Re-enable send button
    sendBtn.disabled = false;
}

// Add message to chat
function addMessage(text, sender) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const avatar = sender === 'user' ? '👤' : '🤖';
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-text">${formatMessage(text)}</div>
            <div class="message-time">${time}</div>
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Format message (convert markdown-like syntax)
function formatMessage(text) {
    // Convert **bold** to <strong>
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert *italic* to <em>
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Convert line breaks
    text = text.replace(/\n/g, '<br>');
    
    // Convert bullet points
    text = text.replace(/^- (.+)$/gm, '<li>$1</li>');
    if (text.includes('<li>')) {
        text = text.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    }
    
    return text;
}

// Show typing indicator
function showTypingIndicator() {
    const messagesContainer = document.getElementById('chat-messages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = 'typing-indicator';
    
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Remove typing indicator
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Update status
function updateStatus(status, text) {
    const statusDot = document.getElementById('status-dot');
    const statusText = document.getElementById('status-text');
    
    statusDot.className = 'status-dot';
    if (status === 'error') {
        statusDot.classList.add('error');
    } else if (status === 'loading') {
        statusDot.classList.add('loading');
    }
    
    statusText.textContent = text;
}

// Get sensor context
async function getSensorContext() {
    try {
        const response = await fetch('/api/sensors');
        const data = await response.json();
        
        return {
            temperature: data.dht22.temperature,
            humidity: data.dht22.humidity,
            airQuality: data.mq135.value,
            soilMoisture: data.fc28.value,
            waterQuality: data.tds.value,
            pm25: data.pms5003.pm25,
            pm10: data.pms5003.pm10,
            location: data.location
        };
    } catch (error) {
        console.error('Error fetching sensor data:', error);
        return null;
    }
}
