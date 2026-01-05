/**
 * Form Display - Manages form rendering and updates
 */

import { formatDate, formatPhone } from './utils.js';

// Field mapping
const fieldMapping = {
    first_name: 'field-first-name',
    last_name: 'field-last-name',
    date_of_birth: 'field-date-of-birth',
    phone: 'field-phone',
    email: 'field-email',
    'address.street': 'field-address-street',
    'address.city': 'field-address-city',
    'address.state': 'field-address-state',
    'address.zip': 'field-address-zip'
};

// Track previously filled fields
const previouslyFilledFields = new Set();

/**
 * Initialize form display
 */
export function initializeFormDisplay() {
    // Form is already in HTML, just need to track state
    previouslyFilledFields.clear();
}

/**
 * Update form with data from state
 * @param {Object} formData - Form data object
 * @param {Object} updatedFields - Recently updated fields (for animations)
 */
export function updateForm(formData, updatedFields = {}) {
    // Update all form fields
    updateField('first_name', formData.first_name);
    updateField('last_name', formData.last_name);
    updateField('date_of_birth', formData.date_of_birth);
    updateField('phone', formData.phone);
    updateField('email', formData.email);

    // Update address fields
    if (formData.address) {
        updateField('address.street', formData.address.street);
        updateField('address.city', formData.address.city);
        updateField('address.state', formData.address.state);
        updateField('address.zip', formData.address.zip);
    }

    // Apply update animations to recently changed fields
    highlightUpdatedFields(updatedFields);

    // Update form status
    updateFormStatus(isFormComplete(formData));
}

/**
 * Update a single field
 * @param {string} fieldName - Field name
 * @param {Object} fieldData - Field data with value and confidence
 */
function updateField(fieldName, fieldData) {
    const elementId = fieldMapping[fieldName];
    if (!elementId) return;

    const element = document.getElementById(elementId);
    if (!element) return;

    // Check if field has value
    if (fieldData && fieldData.value !== null && fieldData.value !== undefined) {
        const value = fieldData.value;
        const confidence = fieldData.confidence || 'high';

        // Format value based on field type
        let displayValue = value;
        if (fieldName === 'date_of_birth') {
            displayValue = formatDate(value);
        } else if (fieldName === 'phone') {
            displayValue = formatPhone(value);
        }

        // Update element content
        element.innerHTML = `<span>${displayValue}</span>`;

        // Add classes
        element.classList.add('has-value');
        element.classList.remove('empty');

        // Add confidence class
        element.classList.remove('confidence-high', 'confidence-medium', 'confidence-low');
        element.classList.add(`confidence-${confidence}`);

        // Track filled field
        previouslyFilledFields.add(fieldName);
    } else {
        // Empty field
        element.innerHTML = '<span class="empty">-</span>';
        element.classList.remove('has-value', 'confidence-high', 'confidence-medium', 'confidence-low');
    }
}

/**
 * Highlight recently updated fields
 * @param {Object} updatedFields - Object with updated field names
 */
function highlightUpdatedFields(updatedFields) {
    // Helper to add animation class
    const animateField = (fieldName, wasPreviouslyFilled) => {
        const elementId = fieldMapping[fieldName];
        if (!elementId) return;

        const element = document.getElementById(elementId);
        if (!element) return;

        // Choose animation based on whether field was previously filled
        const animationClass = wasPreviouslyFilled ? 'corrected' : 'updated';

        // Remove existing animation classes
        element.classList.remove('updated', 'corrected');

        // Trigger reflow to restart animation
        void element.offsetWidth;

        // Add animation class
        element.classList.add(animationClass);

        // Remove animation class after animation completes
        setTimeout(() => {
            element.classList.remove(animationClass);
        }, 1000);
    };

    // Handle top-level fields
    for (const fieldName of Object.keys(updatedFields)) {
        if (fieldName === 'address') {
            // Handle nested address fields
            const addressUpdates = updatedFields.address;
            for (const addrField of Object.keys(addressUpdates)) {
                const fullFieldName = `address.${addrField}`;
                const wasFilled = previouslyFilledFields.has(fullFieldName);
                animateField(fullFieldName, wasFilled);
            }
        } else {
            const wasFilled = previouslyFilledFields.has(fieldName);
            animateField(fieldName, wasFilled);
        }
    }
}

/**
 * Check if form is complete
 * @param {Object} formData - Form data object
 * @returns {boolean} True if all required fields are filled
 */
function isFormComplete(formData) {
    const requiredFields = [
        formData.first_name?.value,
        formData.last_name?.value,
        formData.date_of_birth?.value,
        formData.phone?.value,
        formData.email?.value,
        formData.address?.street?.value,
        formData.address?.city?.value,
        formData.address?.state?.value,
        formData.address?.zip?.value
    ];

    return requiredFields.every(val => val !== null && val !== undefined);
}

/**
 * Update form status indicator
 * @param {boolean} isComplete - Whether form is complete
 */
function updateFormStatus(isComplete) {
    const statusElement = document.getElementById('form-status');
    if (!statusElement) return;

    if (isComplete) {
        statusElement.innerHTML = '<span class="status-complete">Complete</span>';
    } else {
        statusElement.innerHTML = '<span class="status-incomplete">In Progress</span>';
    }
}
