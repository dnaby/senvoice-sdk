"""
Text-to-Speech (TTS) client for SenVoice SDK with async support
"""

import asyncio
import base64
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
        voice: str = "mamito",
        format: str = "opus",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Synthesize text to speech asynchronously (supports French and Wolof)
        
        Args:
            text: Text to synthesize (French or Wolof)
            voice: Voice to use for synthesis (default: "mamito")
            format: Audio format "opus" or "pcm" (default: "opus")
            **kwargs: Additional parameters for synthesis
            
        Returns:
            Synthesis response from the API (contains 'audio' as base64 string for backward compatibility)
            
        Raises:
            ValidationError: If input validation fails
            APIError: If API request fails
        """
        if not text or not isinstance(text, str):
            raise ValidationError("Text must be a non-empty string")
        
        if len(text.strip()) == 0:
            raise ValidationError("Text cannot be empty or whitespace only")
        
        # Collect all chunks from the stream
        audio_chunks = []
        async for chunk in self.synthesize_stream(text, voice, format, **kwargs):
            audio_chunks.append(chunk)
            
        # Combine chunks into a single byte string
        audio_data = b"".join(audio_chunks)
        
        # Encode to base64 for backward compatibility with existing SDK return format
        audio_b64 = base64.b64encode(audio_data).decode('utf-8')
        
        return {
            "text": text,
            "audio": audio_b64,
            "format": format
        }
    
    async def synthesize_stream(
        self, 
        text: str,
        voice: str = "mamito",
        format: str = "opus",
        **kwargs
    ) -> AsyncGenerator[bytes, None]:
        """
        Synthesize text to speech asynchronously with streaming audio output
        
        Args:
            text: Text to synthesize (French or Wolof)
            voice: Voice to use for synthesis (default: "mamito")
            format: Audio format "opus" or "pcm" (default: "opus")
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
            "voice": voice,
            "format": format
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
        voice: str = "mamito",
        format: str = "opus",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Synthesize text to speech asynchronously (supports French and Wolof)
        
        Args:
            text: Text to synthesize (French or Wolof)
            voice: Voice to use for synthesis (default: "mamito")
            format: Audio format "opus" or "pcm" (default: "opus")
            **kwargs: Additional parameters for synthesis
            
        Returns:
            Synthesis response from the API (contains 'audio' as base64 string for backward compatibility)
            
        Raises:
            ValidationError: If input validation fails
            APIError: If API request fails
        """
        if not text or not isinstance(text, str):
            raise ValidationError("Text must be a non-empty string")
        
        if len(text.strip()) == 0:
            raise ValidationError("Text cannot be empty or whitespace only")
        
        # Collect all chunks from the stream
        audio_chunks = []
        async for chunk in self.synthesize_stream(text, voice, format, **kwargs):
            audio_chunks.append(chunk)
            
        # Combine chunks into a single byte string
        audio_data = b"".join(audio_chunks)
        
        # Encode to base64 for backward compatibility with existing SDK return format
        audio_b64 = base64.b64encode(audio_data).decode('utf-8')
        
        return {
            "text": text,
            "audio": audio_b64,
            "format": format
        }
    
    async def synthesize_stream(
        self, 
        text: str,
        voice: str = "mamito",
        format: str = "opus",
        **kwargs
    ) -> AsyncGenerator[bytes, None]:
        """
        Synthesize text to speech asynchronously with streaming audio output (local)
        
        Args:
            text: Text to synthesize (French or Wolof)
            voice: Voice to use for synthesis (default: "mamito")
            format: Audio format "opus" or "pcm" (default: "opus")
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
            "voice": voice,
            "format": format
        }
        
        # Add any additional parameters
        params.update(kwargs)
        
        # Stream the audio response
        async for chunk in self._stream_request('GET', '/tts', params=params):
            yield chunk
