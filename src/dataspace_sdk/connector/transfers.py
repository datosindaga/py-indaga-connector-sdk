from dataspace_sdk.auth.client import DataspaceClient
from dataspace_sdk.model.common import QuerySpecDTO, IdResponseDTO
from dataspace_sdk.model.transfer import TransferProcessDTO, TransferRequestDTO, \
    SuspendTransferDTO

CONTROLLER = "/v1/transferprocess"

def request(client: DataspaceClient, query: QuerySpecDTO) -> list[TransferProcessDTO]:
    response = client.post(
        f"{CONTROLLER}/request",
        json=query.model_dump(by_alias=True),
    )
    return [TransferProcessDTO.model_validate(item) for item in response.json()]


def get_by_id(client: DataspaceClient, id: str) -> TransferProcessDTO:
    response = client.get(f"{CONTROLLER}/{id}")
    return TransferProcessDTO.model_validate(response.json())


def create(client: DataspaceClient, transfer: TransferRequestDTO) -> IdResponseDTO:
    response = client.post(
        CONTROLLER,
        json=transfer.model_dump(by_alias=True),
    )
    return IdResponseDTO.model_validate(response.json())


def resume(client: DataspaceClient, id: str) -> None:
    client.post(f"{CONTROLLER}/{id}/resume")


def suspend(client: DataspaceClient, id: str, suspend_transfer: SuspendTransferDTO) -> None:
    client.post(
        f"{CONTROLLER}/{id}/suspend",
        json=suspend_transfer.model_dump(by_alias=True),
    )


def terminate(client: DataspaceClient, id: str) -> None:
    client.post(f"{CONTROLLER}/{id}/terminate")


def deprovision(client: DataspaceClient, id: str) -> None:
    client.post(f"{CONTROLLER}/{id}/deprovision")