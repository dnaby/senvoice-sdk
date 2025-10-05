"""
SenVoice SDK - Python SDK for RunPod Serverless APIs
"""

from .client import SenVoice
from .tts import TTSClient
from .stt import STTClient, STTWolofClient
from .exceptions import RunPodError, AuthenticationError, APIError, ValidationError

__version__ = "0.1.0"
__author__ = "Mouhamadou Naby DIA"
__email__ = "mouhamadounaby.dia@orange-sonatel.com"

__all__ = [
    "SenVoice",
    "TTSClient", 
    "STTClient",
    "STTWolofClient",
    "RunPodError",
    "AuthenticationError",
    "APIError",
    "ValidationError"
]
