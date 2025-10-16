"""
SenVoice SDK - Python SDK for RunPod Serverless APIs
"""

from .client import SenVoice
from .tts import TTSClient, TTSLocalClient
from .stt import STTClient, STTWolofClient, STTLocalClient, STTWolofLocalClient
from .exceptions import RunPodError, AuthenticationError, APIError, ValidationError

__version__ = "0.2.0"
__author__ = "Mouhamadou Naby DIA"
__email__ = "mouhamadounaby.dia@orange-sonatel.com"

__all__ = [
    "SenVoice",
    "TTSClient",
    "TTSLocalClient", 
    "STTClient",
    "STTWolofClient",
    "STTLocalClient",
    "STTWolofLocalClient",
    "RunPodError",
    "AuthenticationError",
    "APIError",
    "ValidationError"
]
