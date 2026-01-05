from typing import List, Dict, Tuple
from services.llm_service import get_llm_service
from prompts.system_prompt import get_system_prompt
from storage import in_memory_store


class ConversationService:
    """Service for managing conversation flow."""

    def __init__(self):
        """Initialize conversation service."""
        self.llm_service = get_llm_service()
        self.system_prompt = get_system_prompt()

    async def start_conversation(self, session_id: str) -> str:
        """
        Start a new conversation with an initial greeting.

        Args:
            session_id: The session ID

        Returns:
            Initial greeting message
        """
        initial_message = "Hi! I'm here to help you get checked in today. To get started, could you tell me your name?"

        # Add system message and initial assistant message to conversation history
        conversation_history = [
            {"role": "system", "content": self.system_prompt},
            {"role": "assistant", "content": initial_message}
        ]

        in_memory_store.update_session(
            session_id,
            conversation_history=conversation_history
        )

        return initial_message

    async def process_user_message(
        self,
        session_id: str,
        user_message: str
    ) -> Tuple[str, List[Dict]]:
        """
        Process a user message and generate AI response.

        Args:
            session_id: The session ID
            user_message: The user's message

        Returns:
            Tuple of (assistant_response, updated_conversation_history)

        Raises:
            ValueError: If session not found
            Exception: If LLM call fails
        """
        # Get current session
        session = in_memory_store.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        conversation_history = session["conversation_history"]

        # Add user message to history
        conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Generate AI response
        try:
            assistant_response = await self.llm_service.generate_response(
                messages=conversation_history,
                temperature=0.7
            )
        except Exception as e:
            raise Exception(f"Failed to generate response: {str(e)}")

        # Add assistant response to history
        conversation_history.append({
            "role": "assistant",
            "content": assistant_response
        })

        # Update session
        in_memory_store.update_session(
            session_id,
            conversation_history=conversation_history
        )

        return assistant_response, conversation_history

    def get_conversation_for_extraction(self, session_id: str) -> List[Dict]:
        """
        Get conversation history for extraction (without system message).

        Args:
            session_id: The session ID

        Returns:
            Conversation history without system message

        Raises:
            ValueError: If session not found
        """
        session = in_memory_store.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        conversation_history = session["conversation_history"]

        # Remove system message for extraction
        return [msg for msg in conversation_history if msg["role"] != "system"]


# Create singleton instance
conversation_service = ConversationService()


def get_conversation_service() -> ConversationService:
    """Get the conversation service instance."""
    return conversation_service
