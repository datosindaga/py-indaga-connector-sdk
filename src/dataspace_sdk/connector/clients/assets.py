import httpx

from dataspace_sdk.model.asset import AssetOutputDTO, AssetInputDTO
from dataspace_sdk.model.common import QuerySpecDTO, IdResponseDTO


class AssetsClient:
    _controller = "/v1/assets"

    def __init__(self, client: httpx.Client):
        self._client = client

    def request(self, query: QuerySpecDTO) -> list[AssetOutputDTO]:
        """Retrieves a paginated list of assets matching the given query criteria.

        Args:
            query: The query specification defining filters, pagination, and sorting.

        Returns:
            A list of assets matching the criteria. Empty list if none found.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            f"{self._controller}/request",
            json=query,
        )
        return [AssetOutputDTO.model_validate(item) for item in response.json()]

    def get_by_id(self, asset_id: str) -> AssetOutputDTO:
        """Retrieves an asset with the given id.

        Args:
            asset_id: The id of the asset to retrieve.

        Returns:
            The asset.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.get(f"{self._controller}/{asset_id}")
        return AssetOutputDTO.model_validate(response.json())

    def create(self, asset: AssetInputDTO) -> IdResponseDTO:
        """Creates an asset

        Args:
            asset: The asset to create.

        Returns:
            The id.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            self._controller,
            json=asset.model_dump(by_alias=True),
        )
        return IdResponseDTO.model_validate(response.json())

    def update(self, asset: AssetInputDTO) -> None:
        """Updates an asset, targets the asset that matches the inner id.

        Args:
            asset: The asset to update.

        Returns:
            The id.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        self._client.put(
            self._controller,
            json=asset.model_dump(by_alias=True),
        )

    def delete(self, asset_id: str) -> None:
        """Deletes an asset.

        Args:
            asset_id: The id of the asset to delete.

        Returns:
            The id.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        self._client.delete(f"{self._controller}/{asset_id}")