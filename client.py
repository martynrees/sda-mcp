import base64
from typing import Any, Dict, Optional

import httpx

# Constants
AUTH_TIMEOUT = 60.0
REQUEST_TIMEOUT = 30.0


class CatalystCenterClient:
    """Client for interacting with Cisco Catalyst Center API."""

    def __init__(self, base_url: str = None, username: str = None, password: str = None):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = None

    async def authenticate(self) -> bool:
        """Authenticate and get token from Catalyst Center."""
        auth_url = f"{self.base_url}/dna/system/api/v1/auth/token"
        auth_string = f"{self.username}:{self.password}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_auth}"
        }

        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await client.post(auth_url, headers=headers, timeout=AUTH_TIMEOUT)
                response.raise_for_status()
                self.token = response.json().get("Token")
                return bool(self.token)
            except Exception as e:
                print(f"Authentication error: {str(e)}")
                return False

    async def request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Make an API request to Catalyst Center with authentication."""
        if not self.token and not await self.authenticate():
            return None

        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": self.token
        }

        if "headers" in kwargs:
            kwargs["headers"].update(headers)
        else:
            kwargs["headers"] = headers

        kwargs["timeout"] = kwargs.get("timeout", REQUEST_TIMEOUT)

        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await getattr(client, method.lower())(url, **kwargs)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:                    # Token expired, try to re-authenticate
                    if await self.authenticate():
                        # Update headers with new token and retry
                        if "headers" in kwargs:
                            kwargs["headers"]["X-Auth-Token"] = self.token
                        return await self.request(method, endpoint, **kwargs)
                print(f"API error: {str(e)}")
                return None
            except Exception as e:
                print(f"Request error: {str(e)}")
                return None


class ClientManager:
    """Singleton client manager to maintain session state."""
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def set_client(self, client: CatalystCenterClient):
        """Set the active client instance."""
        self._client = client

    def get_client(self) -> Optional[CatalystCenterClient]:
        """Get the active client instance."""
        return self._client

    def clear_client(self):
        """Clear the client instance."""
        self._client = None

    def is_connected(self) -> bool:
        """Check if client is connected and has valid token."""
        return self._client is not None and self._client.token is not None


# Global client manager instance
client_manager = ClientManager()

# Backward compatibility - deprecated, use client_manager instead
client = None
