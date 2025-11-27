// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const userIdInput = document.getElementById('userId');
const activityLog = document.getElementById('activityLog');
const clearLogButton = document.getElementById('clearLogButton');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');

// State
let isProcessing = false;

// Initialize
window.addEventListener('DOMContentLoaded', () => {
    checkApiHealth();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !isProcessing) {
            sendMessage();
        }
    });
    clearLogButton.addEventListener('click', clearActivityLog);
}

// Check API Health
async function checkApiHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'ok') {
            updateStatus(true, 'Connected');
        } else {
            updateStatus(false, 'API Error');
        }
    } catch (error) {
        updateStatus(false, 'Disconnected');
        console.error('Health check failed:', error);
    }
}

// Update Connection Status
function updateStatus(connected, text) {
    statusText.textContent = text;
    if (connected) {
        statusDot.classList.add('connected');
    } else {
        statusDot.classList.remove('connected');
    }
}

// Send Message
async function sendMessage() {
    const message = messageInput.value.trim();
    const userId = userIdInput.value.trim();

    if (!message || !userId) {
        alert('Please enter both User ID and message');
        return;
    }

    if (isProcessing) return;

    // Add user message to chat
    addChatMessage('user', message);
    messageInput.value = '';
    
    // Disable input while processing
    setProcessingState(true);

    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: userId,
                message: message
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        // Add assistant reply
        addChatMessage('assistant', data.reply);
        
        // Process activity log
        if (data.activity_log && data.activity_log.length > 0) {
            processActivityLog(data.activity_log);
        }

    } catch (error) {
        console.error('Error sending message:', error);
        addChatMessage('assistant', '❌ Error: Could not reach the server. Please ensure the backend is running on port 8000.');
        addLogEntry('error', { error: error.message });
    } finally {
        setProcessingState(false);
    }
}

// Add Chat Message
function addChatMessage(role, content) {
    // Remove welcome message if it exists
    const welcomeMsg = chatMessages.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const label = document.createElement('div');
    label.className = 'message-label';
    label.textContent = role === 'user' ? 'You' : 'Assistant';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(label);
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Process Activity Log
function processActivityLog(activities) {
    activities.forEach(activity => {
        const step = activity.step || 'unknown';
        const result = activity.result || {};
        addLogEntry(step, result);
    });
}

// Add Log Entry
function addLogEntry(step, details) {
    // Remove placeholder if it exists
    const placeholder = activityLog.querySelector('.log-placeholder');
    if (placeholder) {
        placeholder.remove();
    }

    const entry = document.createElement('div');
    entry.className = `log-entry ${step}`;
    
    const stepLabel = document.createElement('div');
    stepLabel.className = 'log-step';
    stepLabel.textContent = `🔹 ${step.replace('_', ' ')}`;
    
    const detailsDiv = document.createElement('div');
    detailsDiv.className = 'log-details';
    
    // Format the details nicely
    if (typeof details === 'object') {
        detailsDiv.textContent = JSON.stringify(details, null, 2);
    } else {
        detailsDiv.textContent = details;
    }
    
    entry.appendChild(stepLabel);
    entry.appendChild(detailsDiv);
    activityLog.appendChild(entry);
    
    // Scroll to bottom
    activityLog.scrollTop = activityLog.scrollHeight;
}

// Clear Activity Log
function clearActivityLog() {
    activityLog.innerHTML = '<div class="log-placeholder">Agent activities will appear here...</div>';
}

// Set Processing State
function setProcessingState(processing) {
    isProcessing = processing;
    sendButton.disabled = processing;
    messageInput.disabled = processing;
    sendButton.textContent = processing ? 'Sending...' : 'Send';
}

// Test Scenarios (for demo purposes)
function loadTestScenario(scenario) {
    const scenarios = {
        passwordReset: "I can't log into my account, I think I need a password reset",
        ptoBalance: "How many PTO days do I have left?",
        accountStatus: "Can you check my account status?",
        hrPolicy: "What's the vacation time policy?"
    };
    
    messageInput.value = scenarios[scenario] || '';
}

// Export for console testing
window.testScenarios = {
    passwordReset: () => loadTestScenario('passwordReset'),
    ptoBalance: () => loadTestScenario('ptoBalance'),
    accountStatus: () => loadTestScenario('accountStatus'),
    hrPolicy: () => loadTestScenario('hrPolicy')
};

console.log('💡 Tip: Use window.testScenarios to load demo scenarios');
