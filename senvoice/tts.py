"""
Text-to-Speech (TTS) client for SenVoice SDK with async support
"""

import asyncio
from typing import Dict, Any, Optional, AsyncGenerator
from .base import BaseClient, LocalClient
from .streaming import StreamingMixin
from .exceptions import ValidationError


class TTSClient(BaseClient, StreamingMixin):
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
    
    async def synthesize_stream(
        self, 
        text: str,
        voice: str = "mamito",
        **kwargs
    ) -> AsyncGenerator[bytes, None]:
        """
        Synthesize text to speech asynchronously with streaming audio output
        
        Args:
            text: Text to synthesize (French or Wolof)
            voice: Voice to use for synthesis (default: "mamito")
            **kwargs: Additional parameters for synthesis
            
        Yields:
            Audio chunks as bytes
            
        Raises:
            ValidationError: If input validation fails
            APIError: If API request fails
        """
        if not text or not isinstance(text, str):
            raise ValidationError("Text must be a non-empty string")
        
        if len(text.strip()) == 0:
            raise ValidationError("Text cannot be empty or whitespace only")
        
        # Prepare request parameters for streaming endpoint
        params = {
            "prompt": text,  # Le nouveau modèle utilise 'prompt' au lieu de 'text'
            "voice": voice
        }
        
        # Add any additional parameters
        params.update(kwargs)
        
        # Stream the audio response
        async for chunk in self._stream_request('GET', '/tts', params=params):
            yield chunk


class TTSLocalClient(LocalClient, StreamingMixin):
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
    
    async def synthesize_stream(
        self, 
        text: str,
        voice: str = "mamito",
        **kwargs
    ) -> AsyncGenerator[bytes, None]:
        """
        Synthesize text to speech asynchronously with streaming audio output (local)
        
        Args:
            text: Text to synthesize (French or Wolof)
            voice: Voice to use for synthesis (default: "mamito")
            **kwargs: Additional parameters for synthesis
            
        Yields:
            Audio chunks as bytes
            
        Raises:
            ValidationError: If input validation fails
            APIError: If API request fails
        """
        if not text or not isinstance(text, str):
            raise ValidationError("Text must be a non-empty string")
        
        if len(text.strip()) == 0:
            raise ValidationError("Text cannot be empty or whitespace only")
        
        # Prepare request parameters for streaming endpoint
        params = {
            "prompt": text,  # Le nouveau modèle utilise 'prompt' au lieu de 'text'
            "voice": voice
        }
        
        # Add any additional parameters
        params.update(kwargs)
        
        # Stream the audio response
        async for chunk in self._stream_request('GET', '/tts', params=params):
            yield chunk