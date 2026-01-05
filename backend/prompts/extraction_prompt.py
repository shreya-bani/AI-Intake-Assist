EXTRACTION_PROMPT = """Analyze the conversation history and extract demographic information into a structured JSON format.

Required fields to extract:
- first_name: Patient's first name
- last_name: Patient's last name
- date_of_birth: Date of birth in YYYY-MM-DD format
- phone: Phone number (digits only, no formatting)
- email: Email address
- address: Object with:
  - street: Street address
  - city: City name
  - state: State (2-letter code if possible)
  - zip: ZIP code

Rules for extraction:
1. Only include fields where information was explicitly mentioned
2. If a field was corrected, use the LATEST value provided
3. Use null for fields that haven't been mentioned yet
4. Include a confidence level for each field: "high" (explicitly stated), "medium" (implied or unclear), "low" (guessed)
5. Track which conversation turn number the data came from (1-indexed)
6. Dates should be converted to YYYY-MM-DD format
7. Phone numbers should be digits only (remove spaces, dashes, parentheses)
8. State should be 2-letter code when possible (e.g., "Illinois" -> "IL")

Output format (return ONLY valid JSON, no other text):
{
  "first_name": {"value": "John", "confidence": "high", "turn": 2},
  "last_name": {"value": "Doe", "confidence": "high", "turn": 2},
  "date_of_birth": {"value": "1985-03-15", "confidence": "high", "turn": 3},
  "phone": {"value": "5551234567", "confidence": "high", "turn": 4},
  "email": {"value": "john@example.com", "confidence": "high", "turn": 4},
  "address": {
    "street": {"value": "123 Main St", "confidence": "medium", "turn": 5},
    "city": {"value": "Springfield", "confidence": "high", "turn": 5},
    "state": {"value": "IL", "confidence": "medium", "turn": 5},
    "zip": {"value": "62701", "confidence": "high", "turn": 5}
  }
}

For fields not yet mentioned, use:
"field_name": {"value": null, "confidence": null, "turn": null}

Important:
- Return ONLY the JSON object, no other text
- If a field is corrected, update the value and turn number
- Be conservative with confidence - use "medium" if there's any ambiguity
- Parse dates flexibly (MM/DD/YYYY, MM-DD-YYYY, Month DD, YYYY, etc.) and convert to YYYY-MM-DD
"""


def get_extraction_prompt(conversation_history: list) -> str:
    """
    Create the extraction prompt with conversation history.

    Args:
        conversation_history: List of conversation messages

    Returns:
        Complete prompt with conversation history
    """
    # Format conversation history
    formatted_history = []
    for i, msg in enumerate(conversation_history, 1):
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        formatted_history.append(f"Turn {i} ({role}): {content}")

    history_text = "\n".join(formatted_history)

    return f"""{EXTRACTION_PROMPT}

Conversation history:
{history_text}

Now extract the demographic information as JSON:"""
