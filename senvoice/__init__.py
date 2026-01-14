"""
SenVoice SDK - Python SDK for RunPod Serverless APIs with unified multilingual models
"""

from .client import SenVoice
from .tts import TTSClient, TTSLocalClient
from .stt import STTClient, STTLocalClient
from .exceptions import RunPodError, AuthenticationError, APIError, ValidationError

__version__ = "0.4.0"
__author__ = "Mouhamadou Naby DIA"
__email__ = "mouhamadounaby.dia@orange-sonatel.com"

__all__ = [
    "SenVoice",
    "TTSClient",
    "TTSLocalClient", 
    "STTClient",
    "STTLocalClient",
    "RunPodError",
    "AuthenticationError",
    "APIError",
    "ValidationError"
]
