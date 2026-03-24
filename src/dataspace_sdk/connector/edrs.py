from dataspace_sdk.auth.client import DataspaceClient
from dataspace_sdk.model.common import QuerySpecDTO, DataAddressDTO
from dataspace_sdk.model.edr import EndpointDataReferenceDTO

CONTROLLER = "/v1/edrs"


def request(client: DataspaceClient, query: QuerySpecDTO) -> list[EndpointDataReferenceDTO]:
    response = client.post(
        f"{CONTROLLER}/request",
        json=query.model_dump(by_alias=True),
    )
    return [EndpointDataReferenceDTO.model_validate(item) for item in response.json()]


def get_address(client: DataspaceClient, id: str) -> DataAddressDTO:
    response = client.get(f"{CONTROLLER}/{id}")
    return DataAddressDTO.model_validate(response.json())

# todo Implement a streaming variant for large files in the future
def download(client: DataspaceClient, id: str) -> bytes:
    response = client.get(f"{CONTROLLER}/{id}/download", stream=True)
    response.raise_for_status()
    return response.content


def delete(client: DataspaceClient, id: str) -> None:
    client.delete(f"{CONTROLLER}/{id}")