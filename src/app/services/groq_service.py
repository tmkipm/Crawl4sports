import httpx
from typing import List, Optional, Dict, Any
from datetime import datetime
from ..models.config import GroqConfig
from ..models.integrations import GroqMessage, GroqRequest, GroqResponse, GroqError

class GroqService:
    """Service for interacting with the Groq API."""
    
    def __init__(self, config: GroqConfig):
        """Initialize the Groq service with configuration."""
        self.config = config
        self.client = httpx.AsyncClient(
            base_url=config.base_url,
            headers={
                "Authorization": f"Bearer {config.api_key.get_secret_value()}",
                **config.headers
            },
            timeout=config.timeout
        )

    async def chat_completion(
        self,
        messages: List[GroqMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        stop: Optional[List[str]] = None,
        stream: bool = False
    ) -> GroqResponse:
        """Send a chat completion request to Groq API."""
        request = GroqRequest(
            model=self.config.model,
            messages=messages,
            temperature=temperature or self.config.temperature,
            max_tokens=max_tokens or self.config.max_tokens,
            top_p=top_p or self.config.top_p,
            frequency_penalty=frequency_penalty or self.config.frequency_penalty,
            presence_penalty=presence_penalty or self.config.presence_penalty,
            stop=stop or self.config.stop_sequences,
            stream=stream
        )

        try:
            response = await self.client.post(
                "/openai/v1/chat/completions",
                json=request.dict(exclude_none=True)
            )
            response.raise_for_status()
            return GroqResponse(**response.json())
        except httpx.HTTPStatusError as e:
            raise GroqError(
                error={"message": str(e), "code": e.response.status_code},
                status_code=e.response.status_code
            )
        except Exception as e:
            raise GroqError(
                error={"message": str(e), "code": "unknown"},
                status_code=500
            )

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    @classmethod
    async def create_message(
        cls,
        role: str,
        content: str,
        name: Optional[str] = None
    ) -> GroqMessage:
        """Create a Groq message."""
        return GroqMessage(role=role, content=content, name=name)

    @classmethod
    async def create_system_message(cls, content: str) -> GroqMessage:
        """Create a system message."""
        return await cls.create_message("system", content)

    @classmethod
    async def create_user_message(cls, content: str, name: Optional[str] = None) -> GroqMessage:
        """Create a user message."""
        return await cls.create_message("user", content, name)

    @classmethod
    async def create_assistant_message(cls, content: str) -> GroqMessage:
        """Create an assistant message."""
        return await cls.create_message("assistant", content) 