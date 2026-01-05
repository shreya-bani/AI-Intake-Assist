/**
 * State Manager - Central state management with pub-sub pattern
 */

// Application state
const state = {
    sessionId: null,
    messages: [],
    formData: {},
    isLoading: false,
    error: null
};

// Listeners (subscribers)
const listeners = [];

/**
 * Subscribe to state changes
 * @param {Function} callback - Function to call when state changes
 * @returns {Function} Unsubscribe function
 */
export function subscribe(callback) {
    listeners.push(callback);

    // Return unsubscribe function
    return () => {
        const index = listeners.indexOf(callback);
        if (index > -1) {
            listeners.splice(index, 1);
        }
    };
}

/**
 * Notify all listeners of state change
 */
function notifyListeners() {
    listeners.forEach(callback => callback(state));
}

/**
 * Get current state (readonly)
 * @returns {Object} Current state
 */
export function getState() {
    return { ...state };
}

/**
 * Set session ID
 * @param {string} sessionId - The session ID
 */
export function setSessionId(sessionId) {
    state.sessionId = sessionId;
    notifyListeners();
}

/**
 * Add a message to the conversation
 * @param {string} role - Message role (user or assistant)
 * @param {string} content - Message content
 */
export function addMessage(role, content) {
    const message = {
        role,
        content,
        timestamp: new Date().toISOString()
    };
    state.messages.push(message);
    notifyListeners();
}

/**
 * Update form data
 * @param {Object} updates - Form field updates
 */
export function updateFormData(updates) {
    // Merge updates into form data
    state.formData = {
        ...state.formData,
        ...updates
    };
    notifyListeners();
}

/**
 * Set loading state
 * @param {boolean} loading - Loading state
 */
export function setLoading(loading) {
    state.isLoading = loading;
    notifyListeners();
}

/**
 * Set error
 * @param {string|null} error - Error message or null to clear
 */
export function setError(error) {
    state.error = error;
    notifyListeners();
}

/**
 * Clear error
 */
export function clearError() {
    state.error = null;
    notifyListeners();
}

/**
 * Reset state (for new session or errors)
 */
export function resetState() {
    state.sessionId = null;
    state.messages = [];
    state.formData = {};
    state.isLoading = false;
    state.error = null;
    notifyListeners();
}

/**
 * Initialize state with session data
 * @param {Object} sessionData - Session data from API
 */
export function initializeFromSession(sessionData) {
    state.sessionId = sessionData.session_id;
    state.messages = sessionData.conversation_history || [];
    state.formData = sessionData.form_data || {};
    notifyListeners();
}
