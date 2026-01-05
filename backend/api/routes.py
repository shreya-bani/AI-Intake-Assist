from fastapi import APIRouter, HTTPException
from models.conversation import MessageRequest, MessageResponse
from models.intake_form import (
    SessionCreateResponse,
    SessionStateResponse,
    IntakeFormData
)
from services.conversation_service import get_conversation_service
from services.extraction_service import get_extraction_service
from storage import in_memory_store


router = APIRouter()
conversation_service = get_conversation_service()
extraction_service = get_extraction_service()


@router.post("/sessions", response_model=SessionCreateResponse)
async def create_session():
    """
    Create a new conversation session.

    Returns:
        Session ID and initial greeting message
    """
    try:
        # Create new session in storage
        session_id = in_memory_store.create_session()

        # Start conversation and get initial message
        initial_message = await conversation_service.start_conversation(session_id)

        return SessionCreateResponse(
            session_id=session_id,
            initial_message=initial_message
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@router.post("/sessions/{session_id}/messages", response_model=MessageResponse)
async def send_message(session_id: str, request: MessageRequest):
    """
    Send a user message and get AI response with extracted form data.

    Args:
        session_id: The session ID
        request: Message request with user message

    Returns:
        AI response and updated form fields
    """
    try:
        # Check if session exists
        session = in_memory_store.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Process user message and get AI response
        assistant_response, conversation_history = await conversation_service.process_user_message(
            session_id,
            request.message
        )

        # Extract form data from conversation
        conversation_for_extraction = conversation_service.get_conversation_for_extraction(session_id)
        updated_fields = await extraction_service.extract_form_data(
            session_id,
            conversation_for_extraction
        )

        # Check if form is complete
        session = in_memory_store.get_session(session_id)
        form_data = IntakeFormData(**session["form_data"])
        is_complete = form_data.is_complete()

        return MessageResponse(
            assistant_message=assistant_response,
            updated_fields=updated_fields,
            is_complete=is_complete
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")


@router.get("/sessions/{session_id}", response_model=SessionStateResponse)
async def get_session_state(session_id: str):
    """
    Get the complete state of a session.

    Args:
        session_id: The session ID

    Returns:
        Complete session state including conversation and form data
    """
    try:
        session = in_memory_store.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Check if form is complete
        form_data = IntakeFormData(**session["form_data"])
        is_complete = form_data.is_complete()

        return SessionStateResponse(
            session_id=session["session_id"],
            conversation_history=session["conversation_history"],
            form_data=session["form_data"],
            is_complete=is_complete,
            created_at=session["created_at"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get session: {str(e)}")


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a session.

    Args:
        session_id: The session ID

    Returns:
        Success message
    """
    try:
        success = in_memory_store.delete_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")

        return {"message": "Session deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete session: {str(e)}")
