from typing import Dict, Optional
from datetime import datetime
import uuid
from models.intake_form import IntakeFormData


# In-memory storage for sessions
sessions: Dict[str, dict] = {}


def create_session() -> str:
    """
    Create a new session and return its ID.

    Returns:
        Session ID (UUID)
    """
    session_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    sessions[session_id] = {
        "session_id": session_id,
        "conversation_history": [],
        "form_data": IntakeFormData().model_dump(),
        "created_at": now,
        "last_updated": now
    }

    return session_id


def get_session(session_id: str) -> Optional[dict]:
    """
    Retrieve a session by ID.

    Args:
        session_id: The session ID to retrieve

    Returns:
        Session data dict or None if not found
    """
    return sessions.get(session_id)


def update_session(
    session_id: str,
    conversation_history: Optional[list] = None,
    form_data: Optional[dict] = None
) -> bool:
    """
    Update session data.

    Args:
        session_id: The session ID to update
        conversation_history: New conversation history (optional)
        form_data: New form data (optional)

    Returns:
        True if updated successfully, False if session not found
    """
    session = sessions.get(session_id)
    if not session:
        return False

    if conversation_history is not None:
        session["conversation_history"] = conversation_history

    if form_data is not None:
        session["form_data"] = form_data

    session["last_updated"] = datetime.utcnow().isoformat()
    return True


def delete_session(session_id: str) -> bool:
    """
    Delete a session.

    Args:
        session_id: The session ID to delete

    Returns:
        True if deleted successfully, False if session not found
    """
    if session_id in sessions:
        del sessions[session_id]
        return True
    return False


def get_all_session_ids() -> list:
    """
    Get all session IDs.

    Returns:
        List of session IDs
    """
    return list(sessions.keys())


def clear_all_sessions() -> None:
    """Clear all sessions (useful for testing)."""
    sessions.clear()
