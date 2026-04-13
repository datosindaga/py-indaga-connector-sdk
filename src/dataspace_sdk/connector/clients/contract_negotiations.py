import httpx

from dataspace_sdk.model.common import QuerySpecDTO, IdResponseDTO
from dataspace_sdk.model.contractnegotiation import ContractNegotiationDTO, \
    ContractRequestDTO, NegotiationStateDTO


class ContractNegotiationsClient:
    _controller = "/v1/contractnegotiations"

    def __init__(self, client: httpx.Client):
        self._client = client

    def request(self, query: QuerySpecDTO) -> list[ContractNegotiationDTO]:
        """Retrieves a paginated list of negotiations matching the given query criteria.

        Args:
            query: The query specification defining filters, pagination, and sorting.

        Returns:
            A list of negotiations matching the criteria. Empty list if none found.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            f"{self._controller}/request",
            json=query.model_dump(by_alias=True),
        )
        return [ContractNegotiationDTO.model_validate(item) for item in response.json()]

    def get_by_id(self, contract_id: str) -> ContractNegotiationDTO:
        """Gets a negotiation by its id

        Args:
            contract_id: The id of the negotiation to be retrieved.

        Returns:
            The negotiation with the specified id.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.get(f"{self._controller}/{contract_id}")
        return ContractNegotiationDTO.model_validate(response.json())

    def get_state_by_id(self, contract_id: str) -> NegotiationStateDTO:
        """Gets the state of the negotiation by its id

        Args:
            contract_id: The id of the negotiation to be retrieved.

        Returns:
            The negotiation state.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.get(f"{self._controller}/{contract_id}/state")
        return NegotiationStateDTO.model_validate(response.json())

    def get_agreement(self, contract_id: str) -> ContractNegotiationDTO:
        """Gets the agreement of the negotiation by its id

        Args:
            contract_id: The id of the negotiation to be retrieved.

        Returns:
            The contract agreement that matches that negotiation id.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.get(f"{self._controller}/{contract_id}/agreement")
        return ContractNegotiationDTO.model_validate(response.json())

    def create(self, contract: ContractRequestDTO) -> IdResponseDTO:
        """Creates a new contract negotiation

        Args:
            contract: The contract to be created.

        Returns:
            The id of the created negotiation.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            self._controller,
            json=contract.model_dump(by_alias=True),
        )
        return IdResponseDTO.model_validate(response.json())

    def terminate(self, contract_id: str) -> None:
        """Terminates a negotiation

        Args:
            contract_id: The id of the negotiation to be terminated.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        self._client.post(f"{self._controller}/{contract_id}/terminate")

    def hide(self, contract_id: str) -> None:
        """Hides a negotiation from the user when querying.

        Args:
            contract_id: The id of the negotiation to be hidden.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        self._client.post(f"{self._controller}/{contract_id}/hide")

    def delete(self, contract_id: str) -> None:
        """Deletes a negotiation

        Args:
            contract_id: The id of the negotiation to be deleted

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        self._client.delete(f"{self._controller}/{contract_id}")