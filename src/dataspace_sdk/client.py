import os
from typing import Optional

import httpx

from dataspace_sdk.auth.auth import BasicLoginAuth, TokenAuth
from dataspace_sdk.connector.agreements import AgreementsClient
from dataspace_sdk.connector.assets import AssetsClient
from dataspace_sdk.connector.download import DownloadService
from dataspace_sdk.connector.edrs import EDRSClient
from dataspace_sdk.connector.transfers import TransfersClient

class DataspaceClient:

    def __init__(
        self,
        base_url: str,
        auth: httpx.Auth,
        timeout: float = 10.0,
    ):
        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            auth=auth,
            timeout=timeout,
        )

        # Clients
        self.assets = AssetsClient(self)
        self.agreements = AgreementsClient(self)
        self.transfers = TransfersClient(self)
        self.edrs = EDRSClient(self)

        # Services
        self.downloads = DownloadService(self.agreements, self.transfers, self.edrs)

    @classmethod
    def from_env(
        cls,
        *,
        base_url: str | None = None,
        auth_base_url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        token: str | None = None,
        timeout: float = 10.0,
    ) -> "DataspaceClient":

        resolved_base_url = base_url or os.getenv("DATASPACE_BASE_URL")
        resolved_auth_base_url = auth_base_url or os.getenv("DATASPACE_AUTH_BASE_URL")
        resolved_token = token or os.getenv("DATASPACE_TOKEN")
        resolved_username = username or os.getenv("DATASPACE_USERNAME")
        resolved_password = password or os.getenv("DATASPACE_PASSWORD")

        if not resolved_base_url:
            raise ValueError("Missing DATASPACE_BASE_URL")

        if resolved_token:
            auth = TokenAuth(resolved_token)

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

        return cls(base_url=resolved_base_url, auth=auth, timeout=timeout)

    def get(self, path: str, **kwargs) -> httpx.Response:
        response = self._client.get(path, **kwargs)
        response.raise_for_status()
        return response

    def post(self, path: str, **kwargs) -> httpx.Response:
        response = self._client.post(path, **kwargs)
        response.raise_for_status()
        return response

    def delete(self, path: str, **kwargs) -> httpx.Response:
        response = self._client.delete(path, **kwargs)
        response.raise_for_status()
        return response

    def close(self):
        self._client.close()