"""
Speech-to-Text (STT) client for SenVoice SDK with async support
"""

import base64
from typing import Dict, Any, Optional, Union
from .base import BaseClient, LocalClient
from .exceptions import ValidationError


class STTClient(BaseClient):
    """Async client for unified Speech-to-Text API operations (with authentication)
    Supports both French and Wolof languages automatically
    """
    
    def __init__(self, api_key: str, base_url: str, timeout: int = 60):
        """
        Initialize unified STT client
        
        Args:
            api_key: RunPod API key
            base_url: Base URL for the unified STT API endpoint
            timeout: Request timeout in seconds (default 60 for audio processing)
        """
        super().__init__(api_key, base_url, timeout)
    
    async def transcribe(
        self,
        audio_base64: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Transcribe audio to text asynchronously (supports French and Wolof)
        
        Args:
            audio_base64: Base64 encoded audio data
            **kwargs: Additional parameters for transcription
            
        Returns:
            Transcription response from the API
            
        Raises:
            ValidationError: If input validation fails
            APIError: If API request fails
        """
        if not audio_base64 or not isinstance(audio_base64, str):
            raise ValidationError("audio_base64 must be a non-empty string")
        
        if len(audio_base64.strip()) == 0:
            raise ValidationError("audio_base64 cannot be empty or whitespace only")
        
        # Validate base64 format
        try:
            base64.b64decode(audio_base64, validate=True)
        except Exception:
            raise ValidationError("audio_base64 must be valid base64 encoded data")
        
        # Prepare request data
        data = {
            "audio_base64": audio_base64
        }
        
        # Add any additional parameters
        data.update(kwargs)
        
        return await self._make_request('POST', '/transcribe', data=data)


class STTLocalClient(LocalClient):
    """Async client for unified Speech-to-Text API operations (local, no authentication)
    Supports both French and Wolof languages automatically
    """
    
    def __init__(self, base_url: str, timeout: int = 60):
        """
        Initialize unified local STT client
        
        Args:
            base_url: Base URL for the unified STT API endpoint
            timeout: Request timeout in seconds (default 60 for audio processing)
        """
        super().__init__(base_url, timeout)
    
    async def transcribe(
        self,
        audio_base64: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Transcribe audio to text asynchronously (supports French and Wolof)
        
        Args:
            audio_base64: Base64 encoded audio data
            **kwargs: Additional parameters for transcription
            
        Returns:
            Transcription response from the API
            
        Raises:
            ValidationError: If input validation fails
            APIError: If API request fails
        """
        if not audio_base64 or not isinstance(audio_base64, str):
            raise ValidationError("audio_base64 must be a non-empty string")
        
        if len(audio_base64.strip()) == 0:
            raise ValidationError("audio_base64 cannot be empty or whitespace only")
        
        # Validate base64 format
        try:
            base64.b64decode(audio_base64, validate=True)
        except Exception:
            raise ValidationError("audio_base64 must be valid base64 encoded data")
        
        # Prepare request data
        data = {
            "audio_base64": audio_base64
        }
        
        # Add any additional parameters
        data.update(kwargs)
        
        return await self._make_request('POST', '/transcribe', data=data)
