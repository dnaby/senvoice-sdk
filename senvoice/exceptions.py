"""
Custom exceptions for RunPod SDK
"""


class RunPodError(Exception):
    """Base exception for all RunPod SDK errors"""
    pass


class AuthenticationError(RunPodError):
    """Raised when authentication fails"""
    pass


class APIError(RunPodError):
    """Raised when API request fails"""
    
    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class ValidationError(RunPodError):
    """Raised when input validation fails"""
    pass


class ConnectionError(RunPodError):
    """Raised when connection to API fails"""
    pass
