import httpx

from dataspace_sdk.model.catalog import CatalogRequestDTO, CatalogDTO, \
    DatasetRequestDTO, DatasetDTO, DetailedDatasetDTO, ContactRequestDTO


class CatalogClient:
    _controller = "/v1/catalog"

    def __init__(self, client: httpx.Client):
        self._client = client

    def get_catalog(self, query: CatalogRequestDTO) -> CatalogDTO:
        """Retrieves a single catalog.

        Args:
            query: The query applied to the catalog.

        Returns:
            The catalog.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            f"{self._controller}/request",
            json=query.model_dump(by_alias=True),
        )
        return CatalogDTO.model_validate(response.json())

    def get_dataset(self, query: DatasetRequestDTO) -> DatasetDTO:
        """Retrieves a single dataset.

        Args:
            query: The query applied to the dateset.

        Returns:
            The dataset.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            f"{self._controller}/request/dataset/request",
            json=query.model_dump(by_alias=True),
        )
        return DatasetDTO.model_validate(response.json())

    def get_contact_catalogs(self, query: ContactRequestDTO) -> DetailedDatasetDTO:
        """Retrieves all the catalogs belonging to the registered contacts.

        Args:
            query: The filters applied to the catalog.

        Returns:
            The catalogs.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            f"{self._controller}/request/contacts/request",
            json=query.model_dump(by_alias=True),
        )
        return DetailedDatasetDTO.model_validate(response.json())