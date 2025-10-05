"""
Main SenVoice SDK client with async support
"""

import asyncio
from typing import Optional, Dict, Any
from .tts import TTSClient
from .stt import STTClient, STTWolofClient
from .exceptions import ValidationError


class SenVoice:
    """
    Main SenVoice SDK client that provides access to all async services
    """
    
    def __init__(
        self, 
        api_key: str,
        tts_fr_endpoint_id: Optional[str] = None,
        tts_wo_endpoint_id: Optional[str] = None,
        stt_fr_endpoint_id: Optional[str] = None,
        stt_wo_endpoint_id: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize SenVoice SDK
        
        Args:
            api_key: RunPod API key
            tts_fr_endpoint_id: RunPod endpoint ID for TTS French service
            tts_wo_endpoint_id: RunPod endpoint ID for TTS Wolof service
            stt_fr_endpoint_id: RunPod endpoint ID for STT French service
            stt_wo_endpoint_id: RunPod endpoint ID for STT Wolof service
            timeout: Request timeout in seconds
        """
        if not api_key:
            raise ValidationError("API key is required")
        
        self.api_key = api_key
        self.timeout = timeout
        
        # Initialize service clients
        self._tts_fr_client = None
        self._tts_wo_client = None
        self._stt_fr_client = None
        self._stt_wo_client = None
        
        # Store endpoint IDs and build URLs
        self._tts_fr_endpoint_id = tts_fr_endpoint_id
        self._tts_wo_endpoint_id = tts_wo_endpoint_id
        self._stt_fr_endpoint_id = stt_fr_endpoint_id
        self._stt_wo_endpoint_id = stt_wo_endpoint_id
        
        self._tts_fr_base_url = f"https://{tts_fr_endpoint_id}.api.runpod.ai" if tts_fr_endpoint_id else None
        self._tts_wo_base_url = f"https://{tts_wo_endpoint_id}.api.runpod.ai" if tts_wo_endpoint_id else None
        self._stt_fr_base_url = f"https://{stt_fr_endpoint_id}.api.runpod.ai" if stt_fr_endpoint_id else None
        self._stt_wo_base_url = f"https://{stt_wo_endpoint_id}.api.runpod.ai" if stt_wo_endpoint_id else None
    
    @property
    def tts_fr(self) -> TTSClient:
        """
        Get TTS French client instance
        
        Returns:
            TTSClient instance for French
            
        Raises:
            ValidationError: If TTS French endpoint ID is not configured
        """
        if self._tts_fr_client is None:
            if not self._tts_fr_endpoint_id:
                raise ValidationError(
                    "TTS French endpoint ID is required. Please provide tts_fr_endpoint_id when initializing SenVoice"
                )
            self._tts_fr_client = TTSClient(
                api_key=self.api_key,
                base_url=self._tts_fr_base_url,
                timeout=self.timeout
            )
        return self._tts_fr_client
    
    @property
    def tts_wo(self) -> TTSClient:
        """
        Get TTS Wolof client instance
        
        Returns:
            TTSClient instance for Wolof
            
        Raises:
            ValidationError: If TTS Wolof endpoint ID is not configured
        """
        if self._tts_wo_client is None:
            if not self._tts_wo_endpoint_id:
                raise ValidationError(
                    "TTS Wolof endpoint ID is required. Please provide tts_wo_endpoint_id when initializing SenVoice"
                )
            self._tts_wo_client = TTSClient(
                api_key=self.api_key,
                base_url=self._tts_wo_base_url,
                timeout=self.timeout
            )
        return self._tts_wo_client
    
    @property
    def stt_fr(self) -> STTClient:
        """
        Get STT French client instance
        
        Returns:
            STTClient instance for French
            
        Raises:
            ValidationError: If STT French endpoint ID is not configured
        """
        if self._stt_fr_client is None:
            if not self._stt_fr_endpoint_id:
                raise ValidationError(
                    "STT French endpoint ID is required. Please provide stt_fr_endpoint_id when initializing SenVoice"
                )
            self._stt_fr_client = STTClient(
                api_key=self.api_key,
                base_url=self._stt_fr_base_url,
                timeout=self.timeout
            )
        return self._stt_fr_client
    
    @property
    def stt_wo(self) -> STTWolofClient:
        """
        Get STT Wolof client instance
        
        Returns:
            STTWolofClient instance for Wolof with default sample_rate=16000
            
        Raises:
            ValidationError: If STT Wolof endpoint ID is not configured
        """
        if self._stt_wo_client is None:
            if not self._stt_wo_endpoint_id:
                raise ValidationError(
                    "STT Wolof endpoint ID is required. Please provide stt_wo_endpoint_id when initializing SenVoice"
                )
            self._stt_wo_client = STTWolofClient(
                api_key=self.api_key,
                base_url=self._stt_wo_base_url,
                timeout=self.timeout
            )
        return self._stt_wo_client
    
    def configure_tts_fr(self, endpoint_id: str) -> None:
        """
        Configure TTS French service endpoint ID
        
        Args:
            endpoint_id: RunPod endpoint ID for TTS French service
        """
        if not endpoint_id:
            raise ValidationError("TTS French endpoint ID cannot be empty")
        
        self._tts_fr_endpoint_id = endpoint_id
        self._tts_fr_base_url = f"https://{endpoint_id}.api.runpod.ai"
        self._tts_fr_client = None  # Reset client to use new URL
    
    def configure_tts_wo(self, endpoint_id: str) -> None:
        """
        Configure TTS Wolof service endpoint ID
        
        Args:
            endpoint_id: RunPod endpoint ID for TTS Wolof service
        """
        if not endpoint_id:
            raise ValidationError("TTS Wolof endpoint ID cannot be empty")
        
        self._tts_wo_endpoint_id = endpoint_id
        self._tts_wo_base_url = f"https://{endpoint_id}.api.runpod.ai"
        self._tts_wo_client = None  # Reset client to use new URL
    
    def configure_stt_fr(self, endpoint_id: str) -> None:
        """
        Configure STT French service endpoint ID
        
        Args:
            endpoint_id: RunPod endpoint ID for STT French service
        """
        if not endpoint_id:
            raise ValidationError("STT French endpoint ID cannot be empty")
        
        self._stt_fr_endpoint_id = endpoint_id
        self._stt_fr_base_url = f"https://{endpoint_id}.api.runpod.ai"
        self._stt_fr_client = None  # Reset client to use new URL
    
    def configure_stt_wo(self, endpoint_id: str) -> None:
        """
        Configure STT Wolof service endpoint ID
        
        Args:
            endpoint_id: RunPod endpoint ID for STT Wolof service
        """
        if not endpoint_id:
            raise ValidationError("STT Wolof endpoint ID cannot be empty")
        
        self._stt_wo_endpoint_id = endpoint_id
        self._stt_wo_base_url = f"https://{endpoint_id}.api.runpod.ai"
        self._stt_wo_client = None  # Reset client to use new URL
    
    async def ping_all(self) -> Dict[str, Any]:
        """
        Ping all configured services concurrently
        
        Returns:
            Dictionary with ping results for each service
        """
        tasks = []
        service_names = []
        
        # Create ping tasks for all configured services
        if self._tts_fr_endpoint_id:
            tasks.append(self.tts_fr.ping())
            service_names.append('tts_fr')
        
        if self._tts_wo_endpoint_id:
            tasks.append(self.tts_wo.ping())
            service_names.append('tts_wo')
        
        if self._stt_fr_endpoint_id:
            tasks.append(self.stt_fr.ping())
            service_names.append('stt_fr')
        
        if self._stt_wo_endpoint_id:
            tasks.append(self.stt_wo.ping())
            service_names.append('stt_wo')
        
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
        
        if self._tts_fr_client:
            close_tasks.append(self._tts_fr_client.close())
        if self._tts_wo_client:
            close_tasks.append(self._tts_wo_client.close())
        if self._stt_fr_client:
            close_tasks.append(self._stt_fr_client.close())
        if self._stt_wo_client:
            close_tasks.append(self._stt_wo_client.close())
        
        if close_tasks:
            await asyncio.gather(*close_tasks, return_exceptions=True)
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()