"""
Speech-to-Text (STT) client for SenVoice SDK with async support
"""

import base64
from typing import Dict, Any, Optional, Union
from .base import BaseClient
from .exceptions import ValidationError


class STTClient(BaseClient):
    """Async client for Speech-to-Text API operations"""
    
    def __init__(self, api_key: str, base_url: str, timeout: int = 60):
        """
        Initialize STT client
        
        Args:
            api_key: RunPod API key
            base_url: Base URL for the STT API endpoint
            timeout: Request timeout in seconds (default 60 for audio processing)
        """
        super().__init__(api_key, base_url, timeout)
    
    async def transcribe(
        self,
        audio_base64: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Transcribe audio to text asynchronously
        
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


class STTWolofClient(STTClient):
    """Specialized async STT client for Wolof language with default sample_rate"""
    
    async def transcribe(
        self,
        audio_base64: str,
        sample_rate: int = 16000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Transcribe Wolof audio to text asynchronously
        
        Args:
            audio_base64: Base64 encoded audio data
            sample_rate: Audio sample rate (default: 16000 for Wolof)
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
        
        # Validate sample_rate
        if not isinstance(sample_rate, int) or sample_rate <= 0:
            raise ValidationError("sample_rate must be a positive integer")
        
        # Prepare request data with default sample_rate for Wolof
        data = {
            "audio_base64": audio_base64,
            "sample_rate": sample_rate
        }
        
        # Add any additional parameters
        data.update(kwargs)
        
        return await self._make_request('POST', '/transcribe', data=data)