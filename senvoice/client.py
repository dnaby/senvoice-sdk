"""
Main SenVoice SDK client with async support
"""

import asyncio
from typing import Optional, Dict, Any, Union
from .tts import TTSClient, TTSLocalClient
from .stt import STTClient, STTLocalClient
from .exceptions import ValidationError


class SenVoice:
    """
    Main SenVoice SDK client that provides access to unified ASR and TTS services
    supporting both French and Wolof languages
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        tts_endpoint_id: Optional[str] = None,
        asr_endpoint_id: Optional[str] = None,
        tts_endpoint: Optional[str] = None,
        asr_endpoint: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize SenVoice SDK
        
        Args:
            api_key: RunPod API key (required for RunPod endpoints)
            tts_endpoint_id: RunPod endpoint ID for unified TTS service (French + Wolof)
            asr_endpoint_id: RunPod endpoint ID for unified ASR service (French + Wolof)
            tts_endpoint: Direct URL for unified TTS service (local)
            asr_endpoint: Direct URL for unified ASR service (local)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        
        # Initialize service clients
        self._tts_client = None
        self._asr_client = None
        
        # Store endpoint IDs and direct URLs
        self._tts_endpoint_id = tts_endpoint_id
        self._asr_endpoint_id = asr_endpoint_id
        
        self._tts_endpoint = tts_endpoint
        self._asr_endpoint = asr_endpoint
        
        # Build URLs (priority: direct URL > endpoint_id)
        self._tts_base_url = tts_endpoint or (f"https://{tts_endpoint_id}.api.runpod.ai" if tts_endpoint_id else None)
        self._asr_base_url = asr_endpoint or (f"https://{asr_endpoint_id}.api.runpod.ai" if asr_endpoint_id else None)
        
        # Determine if authentication is needed (RunPod endpoints need auth, local don't)
        self._tts_needs_auth = bool(tts_endpoint_id and not tts_endpoint)
        self._asr_needs_auth = bool(asr_endpoint_id and not asr_endpoint)
    
    @property
    def tts(self) -> Union[TTSClient, TTSLocalClient]:
        """
        Get unified TTS client instance (supports French and Wolof)
        
        Returns:
            TTSClient instance for unified TTS service
            
        Raises:
            ValidationError: If TTS endpoint is not configured
        """
        if self._tts_client is None:
            if not self._tts_base_url:
                raise ValidationError(
                    "TTS endpoint is required. Please provide tts_endpoint_id or tts_endpoint when initializing SenVoice"
                )
            
            # Choose client type based on authentication needs
            if self._tts_needs_auth:
                if not self.api_key:
                    raise ValidationError("API key is required for RunPod endpoints")
                self._tts_client = TTSClient(
                    api_key=self.api_key,
                    base_url=self._tts_base_url,
                    timeout=self.timeout
                )
            else:
                from .tts import TTSLocalClient
                self._tts_client = TTSLocalClient(
                    base_url=self._tts_base_url,
                    timeout=self.timeout
                )
        return self._tts_client
    
    @property
    def asr(self) -> Union[STTClient, STTLocalClient]:
        """
        Get unified ASR client instance (supports French and Wolof)
        
        Returns:
            STTClient instance for unified ASR service
            
        Raises:
            ValidationError: If ASR endpoint is not configured
        """
        if self._asr_client is None:
            if not self._asr_base_url:
                raise ValidationError(
                    "ASR endpoint is required. Please provide asr_endpoint_id or asr_endpoint when initializing SenVoice"
                )
            
            # Choose client type based on authentication needs
            if self._asr_needs_auth:
                if not self.api_key:
                    raise ValidationError("API key is required for RunPod endpoints")
                self._asr_client = STTClient(
                    api_key=self.api_key,
                    base_url=self._asr_base_url,
                    timeout=self.timeout
                )
            else:
                from .stt import STTLocalClient
                self._asr_client = STTLocalClient(
                    base_url=self._asr_base_url,
                    timeout=self.timeout
                )
        return self._asr_client
    
    def configure_tts(self, endpoint_id: str) -> None:
        """
        Configure unified TTS service endpoint ID
        
        Args:
            endpoint_id: RunPod endpoint ID for unified TTS service (French + Wolof)
        """
        if not endpoint_id:
            raise ValidationError("TTS endpoint ID cannot be empty")
        
        self._tts_endpoint_id = endpoint_id
        self._tts_base_url = f"https://{endpoint_id}.api.runpod.ai"
        self._tts_client = None  # Reset client to use new URL
    
    def configure_asr(self, endpoint_id: str) -> None:
        """
        Configure unified ASR service endpoint ID
        
        Args:
            endpoint_id: RunPod endpoint ID for unified ASR service (French + Wolof)
        """
        if not endpoint_id:
            raise ValidationError("ASR endpoint ID cannot be empty")
        
        self._asr_endpoint_id = endpoint_id
        self._asr_base_url = f"https://{endpoint_id}.api.runpod.ai"
        self._asr_client = None  # Reset client to use new URL
    
    async def ping_all(self) -> Dict[str, Any]:
        """
        Ping all configured services concurrently
        
        Returns:
            Dictionary with ping results for each service
        """
        tasks = []
        service_names = []
        
        # Create ping tasks for all configured services
        if self._tts_base_url:
            tasks.append(self.tts.ping())
            service_names.append('tts')
        
        if self._asr_base_url:
            tasks.append(self.asr.ping())
            service_names.append('asr')
        
        # Execute all pings concurrently
        results = {}
        if tasks:
            ping_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for service_name, result in zip(service_names, ping_results):
                if isinstance(result, Exception):
                    results[service_name] = {'error': str(result)}
                else:
                    results[service_name] = result
        
        return results
    
    async def close(self):
        """Close all client sessions"""
        close_tasks = []
        
        if self._tts_client:
            close_tasks.append(self._tts_client.close())
        if self._asr_client:
            close_tasks.append(self._asr_client.close())
        
        if close_tasks:
            await asyncio.gather(*close_tasks, return_exceptions=True)
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()