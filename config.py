from pydantic import BaseModel
from typing import List

class AgentConfig(BaseModel):
    # OpenRouter API configuration
    model: str = "openai/gpt-3.5-turbo"  # OpenRouter model format
    base_url: str = "https://openrouter.ai/api/v1"
    temperature: float = 0.7
    max_tokens: int = 1000
    
    # Agent behavior configuration
    system_prompt: str = """You are a helpful AI assistant that can understand and execute various tasks. 
    You can help with browsing, making reservations, managing files, and performing system operations safely.
    You can analyze user requests and perform appropriate actions."""
    
    # List of allowed commands/operations
    allowed_operations: List[str] = [
        "browse",           # Open websites and web applications
        "search",          # Search the web
        "book",            # Make reservations (restaurants, hotels, etc.)
        "file_read",       # Read files
        "file_write",      # Write files
        "system_cmd",      # Execute system commands
        "calendar",        # Calendar operations
        "email",           # Email operations
        "reminder",        # Set reminders
        "weather",         # Check weather
        "maps",           # Open maps and get directions
        "calculate",       # Perform calculations
    ]
    
    # Application URLs
    app_urls: dict = {
        "google": "https://www.google.com",
        "maps": "https://www.google.com/maps",
        "calendar": "https://calendar.google.com",
        "email": "https://mail.google.com",
        "weather": "https://weather.com",
        "booking": "https://www.opentable.com"
    }
    
    # Safety settings
    max_consecutive_requests: int = 10
    require_confirmation: bool = True
    
    # Output settings
    verbose: bool = True
    show_thinking: bool = True

# Default configuration instance
default_config = AgentConfig() 