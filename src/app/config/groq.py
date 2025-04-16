import os
from ..models.config import GroqConfig

# Get API key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")

# Groq API Configuration
groq_config = GroqConfig(
    api_key=GROQ_API_KEY,  # Now using environment variable
    base_url="https://api.groq.com",
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0.7,
    max_tokens=2048,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop_sequences=None,
    timeout=30,
    max_retries=3,
    retry_delay=1,
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
) 