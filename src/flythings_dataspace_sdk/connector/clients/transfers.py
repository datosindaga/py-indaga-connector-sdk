import httpx

from flythings_dataspace_sdk.model import QuerySpecDTO, TransferProcessDTO, \
    TransferRequestDTO, IdResponseDTO, SuspendTransferDTO, TerminateTransferDTO, PaginatedResultDTO, raise_for_status

class TransfersClient:
    _controller = "/v1/transferprocess"

    def __init__(self, client: httpx.Client):
        self._client = client

    def request(self, query: QuerySpecDTO) -> PaginatedResultDTO[TransferProcessDTO]:
        """Retrieves a paginated list of transfers matching the given query criteria.

        Args:
            query: The query specification defining filters, pagination, and sorting.

        Returns:
            Paginated result containing matching transfers and a flag indicating if more exist.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            f"{self._controller}/request",
            json=query.model_dump(by_alias=True),
        )
        raise_for_status(response)
        return PaginatedResultDTO[TransferProcessDTO].model_validate(response.json())

    def get_by_id(self, transfer_id: str) -> TransferProcessDTO:
        """Retrieves a transfer by its id

        Args:
            transfer_id: The id of the transfer

        Returns:
            The found transfer.

        Raises:
            SdkNotFoundException: If no transfer exists for the given id.
            SdkServerException: If the server returns an unexpected error
        """
        response = self._client.get(f"{self._controller}/{transfer_id}")
        raise_for_status(response)
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
        raise_for_status(response)
        return IdResponseDTO.model_validate(response.json())

    def resume(self, transfer_id: str) -> None:
        """Resumes a transfer

        Args:
            transfer_id: The id of the transfer

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(f"{self._controller}/{transfer_id}/resume")
        raise_for_status(response)

    def suspend(self, transfer_id: str, suspend_transfer: SuspendTransferDTO) -> None:
        """Suspends a transfer

        Args:
            transfer_id: The id of the transfer
            suspend_transfer: the reason

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            f"{self._controller}/{transfer_id}/suspend",
            json=suspend_transfer.model_dump(by_alias=True),
        )
        raise_for_status(response)

    def terminate(self, transfer_id: str, termination: TerminateTransferDTO) -> None:
        """Terminates a transfer

        Args:
            transfer_id: The id of the transfer.
            termination: DTO containing the termination reason and JSON-LD context.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            f"{self._controller}/{transfer_id}/terminate",
            json=termination.model_dump(by_alias=True),
        )
        raise_for_status(response)


    def deprovision(self, transfer_id: str) -> None:
        """Deprovisions a transfer

        Args:
            transfer_id: The id of the transfer

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(f"{self._controller}/{transfer_id}/deprovision")
        raise_for_status(response)