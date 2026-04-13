import os
from typing import Optional

import httpx

from dataspace_sdk.auth.auth import BasicLoginAuth, TokenAuth
from dataspace_sdk.connector.clients.assets import AssetsClient
from dataspace_sdk.connector.clients.catalog import CatalogClient
from dataspace_sdk.connector.clients.contract_agreements import \
    ContractAgreementsClient
from dataspace_sdk.connector.clients.contract_definitions import \
    ContractDefinitionsClient
from dataspace_sdk.connector.clients.contract_negotiations import \
    ContractNegotiationsClient
from dataspace_sdk.connector.clients.edrs import EDRSClient
from dataspace_sdk.connector.clients.policies import PoliciesClient
from dataspace_sdk.connector.clients.transfers import TransfersClient
from dataspace_sdk.connector.services.download import DownloadService
from dataspace_sdk.connector.services.edrs import EdrService
from dataspace_sdk.connector.services.transfer import TransferService


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
        self.assets = AssetsClient(self._client)
        self.policies = PoliciesClient(self._client)
        self.contract_definitions = ContractDefinitionsClient(self._client)
        self.contract_negotiations = ContractNegotiationsClient(self._client)
        self.agreements = ContractAgreementsClient(self._client)
        self.catalog = CatalogClient(self._client)
        self.transfers = TransfersClient(self._client)
        self.edrs = EDRSClient(self._client)

        # Services
        self.download_service = DownloadService(self.agreements, self.transfers, self.edrs)
        self.edr_service = EdrService(self.edrs)
        self.tranfer_service = TransferService(self.transfers, self.edrs)

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
        """
        Creates a new DataspaceClient from environment variables. All values can be overriden.

        Args:
            base_url: Base URL override for this client
            auth_base_url: Base URL override for authentication
            username: Username override for this client
            password: Password override for this client
            token: Token override for this client
            timeout: Timeout override for this client. Defaults to 10
        """
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

    def close(self):
        self._client.close()