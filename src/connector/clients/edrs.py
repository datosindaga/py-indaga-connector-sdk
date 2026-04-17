import httpx

from model.common import QuerySpecDTO, DataAddressDTO
from model.edr import EndpointDataReferenceDTO

class EDRSClient:
    _controller = "/v1/edrs"

    def __init__(self, client: httpx.Client):
        self._client = client

    def request(self, query: QuerySpecDTO) -> list[EndpointDataReferenceDTO]:
        """Retrieves a paginated list of EDRs matching the given query criteria.

        Args:
            query: The query specification defining filters, pagination, and sorting.

        Returns:
            A list of EDRs matching the criteria. Empty list if none found.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            f"{self._controller}/request",
            json=query.model_dump(by_alias=True),
        )
        return [EndpointDataReferenceDTO.model_validate(item) for item in response.json()]


    def get_address(self, transfer_id: str) -> DataAddressDTO:
        """Retrieves the address data of an EDR

        Args:
            transfer_id: The id of the transfer related

        Returns:
            The address data of an EDR

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.get(f"{self._controller}/{transfer_id}")
        return DataAddressDTO.model_validate(response.json())

    def download(self, transfer_id: str) -> bytes:
        """Retrieves the data that an EDR is targeting

        Args:
            transfer_id: The id of the transfer related

        Returns:
            The bytes of the data that an EDR is targeting

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.get(f"{self._controller}/{transfer_id}/download")
        response.raise_for_status()
        return response.content


    def delete(self, transfer_id: str) -> None:
        """Deletes an edr by the transfer id

        Args:
            transfer_id: The id of the transfer related

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        self._client.delete(f"{self._controller}/{transfer_id}")