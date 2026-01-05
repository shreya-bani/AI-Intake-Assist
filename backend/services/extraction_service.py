import json
import re
from typing import Dict, List
from services.llm_service import get_llm_service
from prompts.extraction_prompt import get_extraction_prompt
from models.intake_form import IntakeFormData
from storage import in_memory_store


class ExtractionService:
    """Service for extracting structured data from conversations."""

    def __init__(self):
        """Initialize extraction service."""
        self.llm_service = get_llm_service()

    async def extract_form_data(
        self,
        session_id: str,
        conversation_history: List[Dict]
    ) -> Dict:
        """
        Extract structured form data from conversation history.

        Args:
            session_id: The session ID
            conversation_history: List of conversation messages

        Returns:
            Extracted form data as dictionary

        Raises:
            Exception: If extraction fails
        """
        # Get extraction prompt with conversation history
        extraction_prompt = get_extraction_prompt(conversation_history)

        # Create messages for LLM
        messages = [
            {"role": "user", "content": extraction_prompt}
        ]

        try:
            # Get structured data from LLM
            response = await self.llm_service.extract_structured_data(messages)

            # Parse JSON response
            extracted_data = self._parse_json_response(response)

            # Get previous form data
            session = in_memory_store.get_session(session_id)
            previous_form_data = IntakeFormData(**session["form_data"])

            # Create new form data with extracted information
            new_form_data = self._merge_extracted_data(previous_form_data, extracted_data)

            # Update session with new form data
            in_memory_store.update_session(
                session_id,
                form_data=new_form_data.model_dump()
            )

            # Get updated fields only
            updated_fields = new_form_data.get_updated_fields(previous_form_data)

            return updated_fields

        except Exception as e:
            print(f"Extraction error: {str(e)}")
            # Return empty dict if extraction fails
            return {}

    def _parse_json_response(self, response: str) -> Dict:
        """
        Parse JSON from LLM response, handling various formats.

        Args:
            response: Raw LLM response

        Returns:
            Parsed JSON dictionary

        Raises:
            ValueError: If JSON cannot be parsed
        """
        # Try to extract JSON from response (in case LLM adds extra text)
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass

        # Try parsing the entire response
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON from response: {str(e)}")

    def _merge_extracted_data(
        self,
        previous_data: IntakeFormData,
        extracted_data: Dict
    ) -> IntakeFormData:
        """
        Merge extracted data with previous form data.

        Args:
            previous_data: Previous form data
            extracted_data: Newly extracted data

        Returns:
            Updated IntakeFormData instance
        """
        # Start with previous data
        merged_data = previous_data.model_dump()

        # Update with extracted data
        for field_name, field_value in extracted_data.items():
            if field_name == "address" and isinstance(field_value, dict):
                # Handle nested address fields
                for addr_field, addr_value in field_value.items():
                    if isinstance(addr_value, dict) and addr_value.get("value") is not None:
                        merged_data["address"][addr_field] = addr_value
            elif isinstance(field_value, dict) and field_value.get("value") is not None:
                # Update top-level field if value is not None
                merged_data[field_name] = field_value

        return IntakeFormData(**merged_data)


# Create singleton instance
extraction_service = ExtractionService()


def get_extraction_service() -> ExtractionService:
    """Get the extraction service instance."""
    return extraction_service
