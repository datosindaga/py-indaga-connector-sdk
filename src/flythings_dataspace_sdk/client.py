import os
from typing import Optional

import httpx

from flythings_dataspace_sdk.connector.clients import ContractAgreementsClient, TransfersClient, EDRSClient
from flythings_dataspace_sdk.connector.services import DownloadService
from flythings_dataspace_sdk.auth import TokenAuth, BasicLoginAuth


class DataspaceClient:

    def __init__(
        self,
        base_url: str,
        auth: Optional[httpx.Auth] = None,
        timeout: float = 10.0,
    ):
        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            auth=auth,
            timeout=timeout,
        )

        # Keep reference to auth for refresh logic
        self._auth = auth

        # Clients
        self.agreements = ContractAgreementsClient(self._client)
        self.transfers = TransfersClient(self._client)
        self.edrs = EDRSClient(self._client)

        # Services
        self.download_service = DownloadService(
            self.agreements, self.transfers, self.edrs
        )

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

        auth = None

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

        # NOTE: now allowed to have no auth

        return cls(base_url=resolved_base_url, auth=auth, timeout=timeout)

    # -------------------------
    # Auth management
    # -------------------------

    def set_token(self, token: str):
        """Replace current auth with a static token."""
        self._auth = TokenAuth(token)
        self._client.auth = self._auth

    def set_basic_auth(self, auth_base_url: str, username: str, password: str):
        """Switch to login-based auth."""
        self._auth = BasicLoginAuth(
            auth_base_url=auth_base_url,
            username=username,
            password=password,
        )
        self._client.auth = self._auth

    def clear_auth(self):
        """Remove authentication completely."""
        self._auth = None
        self._client.auth = None

    def refresh_token(self):
        if self._auth is None:
            raise RuntimeError("No auth configured")

        if hasattr(self._auth, "refresh"):
            return self._auth.refresh()

        raise RuntimeError("Current auth does not support refresh")

    def close(self):
        self._client.close()