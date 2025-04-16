from typing import Optional, Dict, List
from pydantic import BaseModel, Field, SecretStr
from .base import BaseDataModel

class APIConfig(BaseDataModel):
    """Model for API configuration."""
    api_key: SecretStr = Field(..., description="API key for authentication")
    base_url: str = Field(..., description="Base URL for the API")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum number of retries")
    retry_delay: int = Field(default=1, description="Delay between retries in seconds")
    headers: Dict[str, str] = Field(
        default_factory=lambda: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        description="Default headers for API requests"
    )

class GroqConfig(APIConfig):
    """Model for Groq API configuration."""
    model: str = Field(..., description="Model to use for completions")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Sampling temperature")
    max_tokens: int = Field(default=2048, description="Maximum number of tokens to generate")
    top_p: float = Field(default=1.0, ge=0.0, le=1.0, description="Nucleus sampling parameter")
    frequency_penalty: float = Field(default=0.0, description="Frequency penalty")
    presence_penalty: float = Field(default=0.0, description="Presence penalty")
    stop_sequences: Optional[List[str]] = Field(None, description="Sequences to stop generation at")

class EnvironmentConfig(BaseDataModel):
    """Model for environment configuration."""
    environment: str = Field(..., description="Current environment (development, staging, production)")
    debug: bool = Field(default=False, description="Whether debug mode is enabled")
    log_level: str = Field(default="INFO", description="Logging level")
    allowed_hosts: List[str] = Field(default=["*"], description="Allowed hosts")
    cors_origins: List[str] = Field(default=["*"], description="CORS allowed origins")
    database_url: SecretStr = Field(..., description="Database connection URL")
    redis_url: Optional[SecretStr] = Field(None, description="Redis connection URL")
    cache_ttl: int = Field(default=3600, description="Default cache TTL in seconds")

class FeatureFlags(BaseDataModel):
    """Model for feature flags."""
    enable_groq: bool = Field(default=True, description="Whether Groq integration is enabled")
    enable_caching: bool = Field(default=True, description="Whether caching is enabled")
    enable_analytics: bool = Field(default=True, description="Whether analytics are enabled")
    enable_notifications: bool = Field(default=True, description="Whether notifications are enabled")
    enable_search: bool = Field(default=True, description="Whether search is enabled")
    enable_betting: bool = Field(default=True, description="Whether betting features are enabled")
    enable_fantasy: bool = Field(default=True, description="Whether fantasy sports features are enabled") 