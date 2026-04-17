import httpx
from model.common import QuerySpecDTO, IdResponseDTO
from model.transfer import TransferProcessDTO, TransferRequestDTO, \
    SuspendTransferDTO

class TransfersClient:
    _controller = "/v1/transferprocess"

    def __init__(self, client: httpx.Client):
        self._client = client

    def request(self, query: QuerySpecDTO) -> list[TransferProcessDTO]:
        """Retrieves a paginated list of transfers matching the given query criteria.

        Args:
            query: The query specification defining filters, pagination, and sorting.

        Returns:
            A list of transfers matching the criteria. Empty list if none found.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            f"{self._controller}/request",
            json=query.model_dump(by_alias=True),
        )
        return [TransferProcessDTO.model_validate(item) for item in response.json()]

    def get_by_id(self, transfer_id: str) -> TransferProcessDTO:
        """Retrieves a transfer by its id

        Args:
            transfer_id: The id of the transfer

        Returns:
            The found transfer.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.get(f"{self._controller}/{transfer_id}")
        return TransferProcessDTO.model_validate(response.json())

    def create(self, transfer: TransferRequestDTO) -> IdResponseDTO:
        """Creates a transfer

        Args:
            transfer: The transfer to be created

        Returns:
            The id of the created transfer.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            self._controller,
            json=transfer.model_dump(by_alias=True),
        )
        return IdResponseDTO.model_validate(response.json())

    def resume(self, transfer_id: str) -> None:
        """Resumes a transfer

        Args:
            transfer_id: The id of the transfer

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        self._client.post(f"{self._controller}/{transfer_id}/resume")

    def suspend(self, transfer_id: str, suspend_transfer: SuspendTransferDTO) -> None:
        """Suspends a transfer

        Args:
            transfer_id: The id of the transfer

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        self._client.post(
            f"{self._controller}/{transfer_id}/suspend",
            json=suspend_transfer.model_dump(by_alias=True),
        )

    def terminate(self, transfer_id: str) -> None:
        """Terminates a transfer

        Args:
            transfer_id: The id of the transfer

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        self._client.post(f"{self._controller}/{transfer_id}/terminate")


    def deprovision(self, transfer_id: str) -> None:
        """Deprovisions a transfer

        Args:
            transfer_id: The id of the transfer

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        self._client.post(f"{self._controller}/{transfer_id}/deprovision")