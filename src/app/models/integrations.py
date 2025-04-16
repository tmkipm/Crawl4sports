from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from .base import BaseDataModel

class GroqMessage(BaseDataModel):
    """Model for Groq chat messages."""
    role: str = Field(..., description="Role of the message sender (system, user, assistant)")
    content: str = Field(..., description="Content of the message")
    name: Optional[str] = Field(None, description="Name of the message sender")

class GroqRequest(BaseDataModel):
    """Model for Groq API requests."""
    model: str = Field(..., description="Model to use for completions")
    messages: List[GroqMessage] = Field(..., description="List of messages in the conversation")
    temperature: Optional[float] = Field(None, ge=0.0, le=1.0, description="Sampling temperature")
    max_tokens: Optional[int] = Field(None, description="Maximum number of tokens to generate")
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0, description="Nucleus sampling parameter")
    frequency_penalty: Optional[float] = Field(None, description="Frequency penalty")
    presence_penalty: Optional[float] = Field(None, description="Presence penalty")
    stop: Optional[List[str]] = Field(None, description="Sequences to stop generation at")
    stream: bool = Field(default=False, description="Whether to stream the response")

class GroqResponse(BaseDataModel):
    """Model for Groq API responses."""
    id: str = Field(..., description="Unique identifier for the completion")
    object: str = Field(..., description="Type of object (chat.completion)")
    created: datetime = Field(..., description="When the completion was created")
    model: str = Field(..., description="Model used for the completion")
    choices: List[Dict[str, Any]] = Field(..., description="List of completion choices")
    usage: Dict[str, int] = Field(..., description="Token usage statistics")

class GroqError(BaseDataModel):
    """Model for Groq API errors."""
    error: Dict[str, Any] = Field(..., description="Error details")
    status_code: int = Field(..., description="HTTP status code")

class WebhookEvent(BaseDataModel):
    """Model for webhook events."""
    event_id: str = Field(..., description="Unique identifier for the event")
    event_type: str = Field(..., description="Type of the event")
    payload: Dict[str, Any] = Field(..., description="Event payload")
    timestamp: datetime = Field(..., description="When the event occurred")
    source: str = Field(..., description="Source of the event")
    signature: Optional[str] = Field(None, description="Event signature for verification")
    attempts: int = Field(default=0, description="Number of processing attempts")
    status: str = Field(..., description="Status of the event (pending, processed, failed)")
    error: Optional[str] = Field(None, description="Error message if processing failed")

class IntegrationStatus(BaseDataModel):
    """Model for integration status."""
    integration_id: str = Field(..., description="Unique identifier for the integration")
    service: str = Field(..., description="Name of the integrated service")
    status: str = Field(..., description="Current status of the integration")
    last_sync: Optional[datetime] = Field(None, description="Last successful sync")
    error_count: int = Field(default=0, description="Number of consecutive errors")
    is_active: bool = Field(..., description="Whether the integration is active")
    config: Dict[str, Any] = Field(..., description="Integration configuration")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata") 