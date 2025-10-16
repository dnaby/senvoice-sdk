"""
Base client for SenVoice SDK with async support
"""

import aiohttp
import asyncio
import json
from typing import Dict, Any, Optional
from .exceptions import AuthenticationError, APIError, ConnectionError


class BaseClient:
    """Base client for making authenticated async requests to RunPod APIs"""
    
    def __init__(self, api_key: str, base_url: str, timeout: int = 30):
        """
        Initialize the base client
        
        Args:
            api_key: RunPod API key
            base_url: Base URL for the API endpoint
            timeout: Request timeout in seconds
        """
        if not api_key:
            raise AuthenticationError("API key is required")
            
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        
        # Default headers for all requests
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        # Session will be created when needed
        self._session = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self._session = aiohttp.ClientSession(
                headers=self.headers,
                timeout=timeout
            )
        return self._session
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an authenticated HTTP request asynchronously
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: JSON data for request body
            params: Query parameters
            
        Returns:
            Response data as dictionary
            
        Raises:
            AuthenticationError: If authentication fails
            APIError: If API request fails
            ConnectionError: If connection fails
        """
        url = f"{self.base_url}{endpoint}"
        session = await self._get_session()
        
        try:
            async with session.request(
                method=method,
                url=url,
                json=data,
                params=params
            ) as response:
                
                # Handle authentication errors
                if response.status == 401:
                    raise AuthenticationError("Invalid API key or authentication failed")
                
                # Handle other HTTP errors
                if response.status >= 400:
                    try:
                        error_data = await response.json()
                        error_message = error_data.get('error', f'HTTP {response.status}')
                    except (json.JSONDecodeError, ValueError):
                        error_text = await response.text()
                        error_message = f'HTTP {response.status}: {error_text}'
                    
                    raise APIError(
                        message=error_message,
                        status_code=response.status,
                        response=response
                    )
                
                # Parse JSON response
                try:
                    return await response.json()
                except (json.JSONDecodeError, ValueError):
                    # If response is not JSON, return raw text
                    response_text = await response.text()
                    return {"response": response_text}
                    
        except asyncio.TimeoutError:
            raise ConnectionError(f"Request timed out after {self.timeout} seconds")
        except aiohttp.ClientConnectionError as e:
            raise ConnectionError(f"Failed to connect to API: {str(e)}")
        except aiohttp.ClientError as e:
            raise APIError(f"Request failed: {str(e)}")
    
    async def ping(self) -> Dict[str, Any]:
        """
        Test API connectivity
        
        Returns:
            Ping response from the API
        """
        return await self._make_request('GET', '/ping')
    
    async def close(self):
        """Close the aiohttp session"""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()


class LocalClient:
    """Base client for making requests to local endpoints (no authentication)"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize the local client
        
        Args:
            base_url: Base URL for the API endpoint
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        
        # Default headers for all requests (no auth)
        self.headers = {
            'Content-Type': 'application/json'
        }
        
        # Session will be created when needed
        self._session = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self._session = aiohttp.ClientSession(
                headers=self.headers,
                timeout=timeout
            )
        return self._session
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request asynchronously (no authentication)
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: JSON data for request body
            params: Query parameters
            
        Returns:
            Response data as dictionary
            
        Raises:
            APIError: If API request fails
            ConnectionError: If connection fails
        """
        url = f"{self.base_url}{endpoint}"
        session = await self._get_session()
        
        try:
            async with session.request(
                method=method,
                url=url,
                json=data,
                params=params
            ) as response:
                
                # Handle HTTP errors
                if response.status >= 400:
                    try:
                        error_data = await response.json()
                        error_message = error_data.get('error', f'HTTP {response.status}')
                    except (json.JSONDecodeError, ValueError):
                        error_text = await response.text()
                        error_message = f'HTTP {response.status}: {error_text}'
                    
                    raise APIError(
                        message=error_message,
                        status_code=response.status,
                        response=response
                    )
                
                # Parse JSON response
                try:
                    return await response.json()
                except (json.JSONDecodeError, ValueError):
                    # If response is not JSON, return raw text
                    response_text = await response.text()
                    return {"response": response_text}
                    
        except asyncio.TimeoutError:
            raise ConnectionError(f"Request timed out after {self.timeout} seconds")
        except aiohttp.ClientConnectionError as e:
            raise ConnectionError(f"Failed to connect to API: {str(e)}")
        except aiohttp.ClientError as e:
            raise APIError(f"Request failed: {str(e)}")
    
    async def ping(self) -> Dict[str, Any]:
        """
        Test API connectivity
        
        Returns:
            Ping response from the API
        """
        return await self._make_request('GET', '/ping')
    
    async def close(self):
        """Close the aiohttp session"""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()