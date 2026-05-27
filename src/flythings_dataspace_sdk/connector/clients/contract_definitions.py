import httpx

from flythings_dataspace_sdk.model import QuerySpecDTO, ContractDefinitionOutputDTO, \
    ContractDefinitionInputDTO, IdResponseDTO, ContractState, PaginatedResultDTO


class ContractDefinitionsClient:
    _controller = "/v1/contractdefinitions"

    def __init__(self, client: httpx.Client):
        self._client = client

    def request(self, query: QuerySpecDTO) -> PaginatedResultDTO[ContractDefinitionOutputDTO]:
        """Retrieves a paginated list of contract definitions matching the given query criteria.

        Args:
            query: The query specification defining filters, pagination, and sorting.

        Returns:
            Paginated result containing matching contract definitions and a flag indicating if more exist.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            f"{self._controller}/request",
            json=query.model_dump(by_alias=True),
        )
        return PaginatedResultDTO[ContractDefinitionOutputDTO].model_validate(response.json())


    def get_by_id(self, contract_id: str) -> ContractDefinitionOutputDTO:
        """Gets a contract by the specified id

        Args:
            contract_id: The id of the contract.

        Returns:
            The contract with the matching id.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.get(f"{self._controller}/{contract_id}")
        return ContractDefinitionOutputDTO.model_validate(response.json())

    def create(self, contract: ContractDefinitionInputDTO) -> IdResponseDTO:
        """Creates a new contract

        Args:
            contract: The contract to be created.

        Returns:
            The id of the created contract.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            self._controller,
            json=contract.model_dump(by_alias=True),
        )
        return IdResponseDTO.model_validate(response.json())

    def update(self, contract: ContractDefinitionInputDTO) -> None:
        """Updates a contract, targets the contract with the given inner id.

        Args:
            contract: The contract to be updated.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        self._client.put(
            self._controller,
            json=contract.model_dump(by_alias=True),
        )

    def change_state(self, contract_id: str, state: ContractState) -> None:
        """Changes the state of a contract.

        Args:
            contract_id: The id of the contract.
            state: The new state of the contract.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        self._client.put(
            f"{self._controller}/state/{contract_id}",
            content=state.value.encode(),
            headers={"Content-Type": "text/plain"},
        )

    def delete(self, contract_id: str) -> None:
        """Deletes a contract

        Args:
            contract_id: The id of the contract to be deleted.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        self._client.delete(f"{self._controller}/{contract_id}")