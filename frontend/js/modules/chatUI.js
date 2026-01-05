/**
 * Chat UI - Manages chat interface rendering and interactions
 */

import { formatTime } from './utils.js';

// DOM elements
let chatMessagesContainer;
let chatInput;
let sendButton;
let loadingIndicator;

/**
 * Initialize chat UI
 */
export function initializeChatUI() {
    chatMessagesContainer = document.getElementById('chat-messages');
    chatInput = document.getElementById('chat-input');
    sendButton = document.getElementById('send-button');
    loadingIndicator = document.getElementById('loading-indicator');

    // Enable send button and input
    setInputEnabled(true);
}

/**
 * Render messages from state
 * @param {Array} messages - Array of message objects
 */
export function renderMessages(messages) {
    // Clear existing messages
    chatMessagesContainer.innerHTML = '';

    if (messages.length === 0) {
        chatMessagesContainer.innerHTML = '<div class="chat-empty">Your conversation will appear here</div>';
        return;
    }

    // Render each message (skip system messages)
    messages.forEach(msg => {
        if (msg.role !== 'system') {
            appendMessage(msg.role, msg.content, msg.timestamp);
        }
    });

    // Scroll to bottom
    scrollToBottom();
}

/**
 * Append a single message to the chat
 * @param {string} role - Message role (user or assistant)
 * @param {string} content - Message content
 * @param {string} timestamp - Message timestamp (optional)
 */
export function appendMessage(role, content, timestamp) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    bubbleDiv.textContent = content;

    messageDiv.appendChild(bubbleDiv);

    // Add timestamp if provided
    if (timestamp) {
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = formatTime(timestamp);
        messageDiv.appendChild(timeDiv);
    }

    chatMessagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Get current input value
 * @returns {string} Current input text
 */
export function getInputValue() {
    return chatInput.value.trim();
}

/**
 * Clear input field
 */
export function clearInput() {
    chatInput.value = '';
}

/**
 * Set loading state
 * @param {boolean} loading - Whether loading is active
 */
export function setLoading(loading) {
    if (loading) {
        loadingIndicator.style.display = 'flex';
        setInputEnabled(false);
    } else {
        loadingIndicator.style.display = 'none';
        setInputEnabled(true);
    }
}

/**
 * Enable or disable input and send button
 * @param {boolean} enabled - Whether input should be enabled
 */
export function setInputEnabled(enabled) {
    chatInput.disabled = !enabled;
    sendButton.disabled = !enabled;

    if (enabled) {
        chatInput.focus();
    }
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
}

/**
 * Show error in chat
 * @param {string} errorMessage - Error message to display
 */
export function showChatError(errorMessage) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'message assistant';
    errorDiv.innerHTML = `
        <div class="message-bubble" style="background-color: #fee2e2; color: #991b1b;">
            Error: ${errorMessage}
        </div>
    `;
    chatMessagesContainer.appendChild(errorDiv);
    scrollToBottom();
}

/**
 * Setup event listeners for chat input
 * @param {Function} onSendMessage - Callback when message is sent
 */
export function setupChatListeners(onSendMessage) {
    // Send button click
    sendButton.addEventListener('click', () => {
        const message = getInputValue();
        if (message) {
            onSendMessage(message);
        }
    });

    // Enter key press
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const message = getInputValue();
            if (message) {
                onSendMessage(message);
            }
        }
    });
}
