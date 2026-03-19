"""
Auto-generated gRPC FastAPI client
Generated from services.json
"""

import logging
from typing import Any, Dict, Optional
from urllib.parse import urlparse, urlunparse

import httpx
from authlib.integrations.requests_client import OAuth2Session
from pydantic import BaseModel

# Import all required models

logger = logging.getLogger(__name__)


class EmptyRequest(BaseModel):
    """Empty request model for health check"""

    pass


class Client:
    """Generated gRPC FastAPI client with type safety"""

    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        openid_discovery_url: str,
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client_id = client_id
        self._client_secret = client_secret
        openid_configuration = httpx.get(openid_discovery_url).json()
        self._token_url = openid_configuration.get("token_endpoint")
        client = OAuth2Session(client_id, client_secret)

        # 获取 Acce ss Token (Client Credentials Flow)
        self._default_token = client.fetch_token(
            url=self._token_url,
            grant_type="client_credentials",
            client_id=client_id,
            client_secret=client_secret,
        )

    def _build_headers(
        self, extra_headers: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """Build request headers with authentication"""
        headers = {}
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def _build_websocket_uri(self, path: str) -> str:
        """Build WebSocket URI from HTTP base URL"""
        parsed = urlparse(self.base_url)
        ws_scheme = "wss" if parsed.scheme == "https" else "ws"
        return urlunparse(
            (
                ws_scheme,
                parsed.netloc,
                path.lstrip("/"),
                parsed.params,
                parsed.query,
                parsed.fragment,
            )
        )
