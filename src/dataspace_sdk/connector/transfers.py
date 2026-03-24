import httpx
from dataspace_sdk.model.common import QuerySpecDTO, IdResponseDTO
from dataspace_sdk.model.transfer import TransferProcessDTO, TransferRequestDTO, \
    SuspendTransferDTO

class TransfersClient:
    _controller = "/v1/transferprocess"

    def __init__(self, client: httpx.Client):
        self._client = client

    def request(self, query: QuerySpecDTO) -> list[TransferProcessDTO]:
        response = self._client.post(
            f"{self._controller}/request",
            json=query.model_dump(by_alias=True),
        )
        return [TransferProcessDTO.model_validate(item) for item in response.json()]


    def get_by_id(self, transfer_id: str) -> TransferProcessDTO:
        response = self._client.get(f"{self._controller}/{transfer_id}")
        return TransferProcessDTO.model_validate(response.json())


    def create(self, transfer: TransferRequestDTO) -> IdResponseDTO:
        response = self._client.post(
            self._controller,
            json=transfer.model_dump(by_alias=True),
        )
        return IdResponseDTO.model_validate(response.json())


    def resume(self, transfer_id: str) -> None:
        self._client.post(f"{self._controller}/{transfer_id}/resume")


    def suspend(self, transfer_id: str, suspend_transfer: SuspendTransferDTO) -> None:
        self._client.post(
            f"{self._controller}/{transfer_id}/suspend",
            json=suspend_transfer.model_dump(by_alias=True),
        )


    def terminate(self, transfer_id: str) -> None:
        self._client.post(f"{self._controller}/{transfer_id}/terminate")


    def deprovision(self, transfer_id: str) -> None:
        self._client.post(f"{self._controller}/{transfer_id}/deprovision")