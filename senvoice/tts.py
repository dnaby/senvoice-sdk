"""
Text-to-Speech (TTS) client for SenVoice SDK with async support
"""

from typing import Dict, Any, Optional
from .base import BaseClient, LocalClient
from .exceptions import ValidationError


class TTSClient(BaseClient):
    """Async client for unified Text-to-Speech API operations (with authentication)
    Supports both French and Wolof languages automatically
    """
    
    def __init__(self, api_key: str, base_url: str, timeout: int = 30):
        """
        Initialize unified TTS client
        
        Args:
            api_key: RunPod API key
            base_url: Base URL for the unified TTS API endpoint
            timeout: Request timeout in seconds
        """
        super().__init__(api_key, base_url, timeout)
    
    async def synthesize(
        self, 
        text: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Synthesize text to speech asynchronously (supports French and Wolof)
        
        Args:
            text: Text to synthesize (French or Wolof)
            **kwargs: Additional parameters for synthesis
            
        Returns:
            Synthesis response from the API
            
        Raises:
            ValidationError: If input validation fails
            APIError: If API request fails
        """
        if not text or not isinstance(text, str):
            raise ValidationError("Text must be a non-empty string")
        
        if len(text.strip()) == 0:
            raise ValidationError("Text cannot be empty or whitespace only")
        
        # Prepare request data
        data = {
            "text": text
        }
        
        # Add any additional parameters
        data.update(kwargs)
        
        return await self._make_request('POST', '/synthesize', data=data)


class TTSLocalClient(LocalClient):
    """Async client for unified Text-to-Speech API operations (local, no authentication)
    Supports both French and Wolof languages automatically
    """
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize unified local TTS client
        
        Args:
            base_url: Base URL for the unified TTS API endpoint
            timeout: Request timeout in seconds
        """
        super().__init__(base_url, timeout)
    
    async def synthesize(
        self, 
        text: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Synthesize text to speech asynchronously (supports French and Wolof)
        
        Args:
            text: Text to synthesize (French or Wolof)
            **kwargs: Additional parameters for synthesis
            
        Returns:
            Synthesis response from the API
            
        Raises:
            ValidationError: If input validation fails
            APIError: If API request fails
        """
        if not text or not isinstance(text, str):
            raise ValidationError("Text must be a non-empty string")
        
        if len(text.strip()) == 0:
            raise ValidationError("Text cannot be empty or whitespace only")
        
        # Prepare request data
        data = {
            "text": text
        }
        
        # Add any additional parameters
        data.update(kwargs)
        
        return await self._make_request('POST', '/synthesize', data=data)