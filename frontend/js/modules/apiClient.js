/**
 * API Client - Handles all HTTP requests to the backend
 */

// API base URL - adjust based on environment
const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Create a new conversation session
 * @returns {Promise<Object>} Session data with session_id and initial_message
 * @throws {Error} If request fails
 */
export async function createSession() {
    try {
        const response = await fetch(`${API_BASE_URL}/sessions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create session');
        }

        return await response.json();
    } catch (error) {
        throw new Error(`Failed to create session: ${error.message}`);
    }
}

/**
 * Send a message to the AI assistant
 * @param {string} sessionId - The session ID
 * @param {string} message - User message
 * @returns {Promise<Object>} Response with assistant_message, updated_fields, is_complete
 * @throws {Error} If request fails
 */
export async function sendMessage(sessionId, message) {
    try {
        const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}/messages`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to send message');
        }

        return await response.json();
    } catch (error) {
        throw new Error(`Failed to send message: ${error.message}`);
    }
}

/**
 * Get session state
 * @param {string} sessionId - The session ID
 * @returns {Promise<Object>} Session state with conversation and form data
 * @throws {Error} If request fails
 */
export async function getSessionState(sessionId) {
    try {
        const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to get session state');
        }

        return await response.json();
    } catch (error) {
        throw new Error(`Failed to get session state: ${error.message}`);
    }
}

/**
 * Delete a session
 * @param {string} sessionId - The session ID
 * @returns {Promise<Object>} Success message
 * @throws {Error} If request fails
 */
export async function deleteSession(sessionId) {
    try {
        const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to delete session');
        }

        return await response.json();
    } catch (error) {
        throw new Error(`Failed to delete session: ${error.message}`);
    }
}

/**
 * Check API health
 * @returns {Promise<Object>} Health status
 */
export async function checkHealth() {
    try {
        const response = await fetch(`http://localhost:8000/api/health`, {
            method: 'GET'
        });

        if (!response.ok) {
            throw new Error('Health check failed');
        }

        return await response.json();
    } catch (error) {
        throw new Error(`Health check failed: ${error.message}`);
    }
}
