from pydantic import BaseModel, Field
from typing import Optional, Literal


class FieldValue(BaseModel):
    """A single form field value with metadata."""
    value: Optional[str] = None
    confidence: Optional[Literal["high", "medium", "low"]] = None
    turn: Optional[int] = None


class Address(BaseModel):
    """Address information."""
    street: FieldValue = Field(default_factory=FieldValue)
    city: FieldValue = Field(default_factory=FieldValue)
    state: FieldValue = Field(default_factory=FieldValue)
    zip: FieldValue = Field(default_factory=FieldValue)


class IntakeFormData(BaseModel):
    """Complete intake form data structure."""
    first_name: FieldValue = Field(default_factory=FieldValue)
    last_name: FieldValue = Field(default_factory=FieldValue)
    date_of_birth: FieldValue = Field(default_factory=FieldValue)
    phone: FieldValue = Field(default_factory=FieldValue)
    email: FieldValue = Field(default_factory=FieldValue)
    address: Address = Field(default_factory=Address)

    def is_complete(self) -> bool:
        """Check if all required fields have values."""
        required_fields = [
            self.first_name.value,
            self.last_name.value,
            self.date_of_birth.value,
            self.phone.value,
            self.email.value,
            self.address.street.value,
            self.address.city.value,
            self.address.state.value,
            self.address.zip.value
        ]
        return all(field is not None for field in required_fields)

    def get_updated_fields(self, previous_data: "IntakeFormData") -> dict:
        """
        Compare with previous data and return only updated fields.

        Args:
            previous_data: Previous version of the form data

        Returns:
            Dictionary of updated fields
        """
        updated = {}

        # Check top-level fields
        for field_name in ["first_name", "last_name", "date_of_birth", "phone", "email"]:
            current_field = getattr(self, field_name)
            previous_field = getattr(previous_data, field_name)

            if current_field.value != previous_field.value:
                updated[field_name] = current_field.model_dump()

        # Check address fields
        address_updated = {}
        for addr_field in ["street", "city", "state", "zip"]:
            current_addr = getattr(self.address, addr_field)
            previous_addr = getattr(previous_data.address, addr_field)

            if current_addr.value != previous_addr.value:
                address_updated[addr_field] = current_addr.model_dump()

        if address_updated:
            updated["address"] = address_updated

        return updated


class SessionData(BaseModel):
    """Complete session data including conversation and form."""
    session_id: str
    conversation_history: list = Field(default_factory=list)
    form_data: IntakeFormData = Field(default_factory=IntakeFormData)
    created_at: str
    last_updated: str


class SessionCreateResponse(BaseModel):
    """Response when creating a new session."""
    session_id: str
    initial_message: str


class SessionStateResponse(BaseModel):
    """Response with complete session state."""
    session_id: str
    conversation_history: list
    form_data: dict
    is_complete: bool
    created_at: str
