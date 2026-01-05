/**
 * Main Application Entry Point
 */

import * as StateManager from './modules/stateManager.js';
import * as APIClient from './modules/apiClient.js';
import * as ChatUI from './modules/chatUI.js';
import * as FormDisplay from './modules/formDisplay.js';

/**
 * Initialize the application
 */
async function initializeApp() {
    try {
        // Initialize UI components
        ChatUI.initializeChatUI();
        FormDisplay.initializeFormDisplay();

        // Subscribe to state changes
        StateManager.subscribe(onStateChange);

        // Setup chat event listeners
        ChatUI.setupChatListeners(handleSendMessage);

        // Setup error modal
        setupErrorModal();

        // Create new session
        await createNewSession();

    } catch (error) {
        showError(`Failed to initialize application: ${error.message}`);
    }
}

/**
 * Create a new conversation session
 */
async function createNewSession() {
    try {
        ChatUI.setLoading(true);

        // Call API to create session
        const sessionData = await APIClient.createSession();

        // Update state
        StateManager.setSessionId(sessionData.session_id);
        StateManager.addMessage('assistant', sessionData.initial_message);

        // Update UI to show session ID
        document.getElementById('session-id').textContent =
            sessionData.session_id.slice(0, 8) + '...';

        ChatUI.setLoading(false);

    } catch (error) {
        ChatUI.setLoading(false);
        showError(`Failed to create session: ${error.message}`);
    }
}

/**
 * Handle sending a message
 * @param {string} message - User message
 */
async function handleSendMessage(message) {
    try {
        const state = StateManager.getState();

        if (!state.sessionId) {
            showError('No active session. Please refresh the page.');
            return;
        }

        // Add user message to state
        StateManager.addMessage('user', message);

        // Clear input
        ChatUI.clearInput();

        // Set loading state
        StateManager.setLoading(true);

        // Send message to API
        const response = await APIClient.sendMessage(state.sessionId, message);

        // Add assistant response to state
        StateManager.addMessage('assistant', response.assistant_message);

        // Update form data if there are updates
        if (response.updated_fields && Object.keys(response.updated_fields).length > 0) {
            StateManager.updateFormData(response.updated_fields);
        }

        // Clear loading state
        StateManager.setLoading(false);

    } catch (error) {
        StateManager.setLoading(false);
        showError(`Failed to send message: ${error.message}`);
        ChatUI.showChatError(error.message);
    }
}

/**
 * Handle state changes
 * @param {Object} state - Current application state
 */
function onStateChange(state) {
    // Update chat UI
    ChatUI.renderMessages(state.messages);
    ChatUI.setLoading(state.isLoading);

    // Update form display
    FormDisplay.updateForm(state.formData, state.formData);

    // Show error if present
    if (state.error) {
        showError(state.error);
    }
}

/**
 * Setup error modal
 */
function setupErrorModal() {
    const errorModal = document.getElementById('error-modal');
    const errorClose = document.getElementById('error-close');

    if (errorClose) {
        errorClose.addEventListener('click', () => {
            errorModal.style.display = 'none';
            StateManager.clearError();
        });
    }

    // Close modal when clicking outside
    errorModal.addEventListener('click', (e) => {
        if (e.target === errorModal) {
            errorModal.style.display = 'none';
            StateManager.clearError();
        }
    });
}

/**
 * Show error modal
 * @param {string} errorMessage - Error message to display
 */
function showError(errorMessage) {
    const errorModal = document.getElementById('error-modal');
    const errorMessageElement = document.getElementById('error-message');

    if (errorMessageElement) {
        errorMessageElement.textContent = errorMessage;
    }

    if (errorModal) {
        errorModal.style.display = 'flex';
    }

    StateManager.setError(errorMessage);
}

/**
 * Handle page visibility change (pause/resume)
 */
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        // Page became visible - could refresh session state here
        console.log('Page visible');
    }
});

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}
