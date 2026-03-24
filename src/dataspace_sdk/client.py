import os
from typing import Optional

import httpx

from dataspace_sdk.auth.auth import Auth, BasicLoginAuth, TokenAuth
from dataspace_sdk.connector.agreements import AgreementsClient
from dataspace_sdk.connector.assets import AssetsClient
from dataspace_sdk.connector.download import DownloadService
from dataspace_sdk.connector.edrs import EDRSClient
from dataspace_sdk.connector.transfers import TransfersClient

class DataspaceClient:
    def __init__(
        self,
        base_url: str,
        auth: Auth,
        timeout: float = 10.0,
    ):
        self._auth = auth
        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            timeout=timeout,
        )

        # Clients
        self.assets = AssetsClient(self._client)
        self.agreements = AgreementsClient(self._client)
        self.transfers = TransfersClient(self._client)
        self.edrs = EDRSClient(self._client)

        # Services
        self.downloads = DownloadService(self.agreements, self.transfers, self.edrs)

    @classmethod
    def from_env(
        cls,
        *,
        base_url: Optional[str] = None,
        auth_base_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
        timeout: float = 10.0,
    ) -> "DataspaceClient":

        resolved_base_url = base_url or os.getenv("DATASPACE_BASE_URL")
        resolved_auth_base_url = auth_base_url or os.getenv("DATASPACE_AUTH_BASE_URL")
        resolved_token = token or os.getenv("DATASPACE_TOKEN")
        resolved_username = username or os.getenv("DATASPACE_USERNAME")
        resolved_password = password or os.getenv("DATASPACE_PASSWORD")

        if not resolved_base_url:
            raise ValueError("Missing DATASPACE_BASE_URL")

        # 1️⃣ Token has priority
        if resolved_token:
            auth = TokenAuth(resolved_token)

        # 2️⃣ Username/password → GET login via basic auth
        elif resolved_username and resolved_password:
            if not resolved_auth_base_url:
                raise ValueError("Missing DATASPACE_AUTH_BASE_URL")

            auth = BasicLoginAuth(
                auth_base_url=resolved_auth_base_url,
                username=resolved_username,
                password=resolved_password,
            )

        else:
            raise ValueError(
                "Provide DATASPACE_TOKEN or "
                "DATASPACE_USERNAME + DATASPACE_PASSWORD"
            )

        return cls(
            base_url=resolved_base_url,
            auth=auth,
            timeout=timeout,
        )

    def _request(self, method: str, path: str, **kwargs):
        headers = kwargs.pop("headers", {})
        headers.update(self._auth.get_headers())

        response = self._client.request(
            method,
            path,
            headers=headers,
            **kwargs,
        )
        response.raise_for_status()
        return response

    def get(self, path: str, **kwargs):
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self._request("POST", path, **kwargs)

    def close(self):
        self._client.close()