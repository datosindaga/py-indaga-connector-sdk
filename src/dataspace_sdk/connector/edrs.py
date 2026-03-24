import httpx

from dataspace_sdk.model.common import QuerySpecDTO, DataAddressDTO
from dataspace_sdk.model.edr import EndpointDataReferenceDTO

class EDRSClient:
    _controller = "/v1/edrs"

    def __init__(self, client: httpx.Client):
        self._client = client

    def request(self, query: QuerySpecDTO) -> list[EndpointDataReferenceDTO]:
        response = self._client.post(
            f"{self._controller}/request",
            json=query.model_dump(by_alias=True),
        )
        return [EndpointDataReferenceDTO.model_validate(item) for item in response.json()]


    def get_address(self, transfer_id: str) -> DataAddressDTO:
        response = self._client.get(f"{self._controller}/{transfer_id}")
        return DataAddressDTO.model_validate(response.json())

    # todo Implement a streaming variant for large files in the future
    def download(self, transfer_id: str) -> bytes:
        response = self._client.get(f"{self._controller}/{transfer_id}/download")
        response.raise_for_status()
        return response.content


    def delete(self, transfer_id: str) -> None:
        self._client.delete(f"{self._controller}/{transfer_id}")