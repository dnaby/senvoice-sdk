"""
Streaming utilities for SenVoice SDK
"""

import asyncio
import json
from typing import Dict, Any, Optional, AsyncGenerator
import aiohttp
from .exceptions import AuthenticationError, APIError, ConnectionError


class StreamingMixin:
    """Mixin class to add streaming capabilities to clients"""
    
    async def _stream_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[bytes, None]:
        """
        Make a streaming HTTP request asynchronously
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: JSON data for request body
            params: Query parameters
            
        Yields:
            Response chunks as bytes
            
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
                
                # Stream the response content
                async for chunk in response.content.iter_chunked(8192):
                    if chunk:
                        yield chunk
                        
        except asyncio.TimeoutError:
            raise ConnectionError(f"Request timed out after {self.timeout} seconds")
        except aiohttp.ClientConnectionError as e:
            raise ConnectionError(f"Failed to connect to API: {str(e)}")
        except aiohttp.ClientError as e:
            raise APIError(f"Request failed: {str(e)}")
