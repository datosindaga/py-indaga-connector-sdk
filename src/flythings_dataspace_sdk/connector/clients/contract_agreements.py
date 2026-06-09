import httpx

from flythings_dataspace_sdk.model import QuerySpecDTO, ContractAgreementDTO, \
    ContractNegotiationDTO, PaginatedResultDTO, raise_for_status

class ContractAgreementsClient:
    _controller = "/v1/contractagreements"

    def __init__(self, client: httpx.Client):
        self._client = client

    def request(self, query: QuerySpecDTO) -> PaginatedResultDTO[ContractAgreementDTO]:
        """Retrieves a paginated list of contract agreements matching the given query criteria.

        Args:
            query: The query specification defining filters, pagination, and sorting.

        Returns:
            Paginated result containing matching contract agreements and a flag indicating if more exist.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            f"{self._controller}/request",
            json=query.model_dump(by_alias=True),
        )
        raise_for_status(response)
        return PaginatedResultDTO[ContractAgreementDTO].model_validate(response.json())


    def get_by_id(self, agreement_id: str) -> ContractAgreementDTO:
        """Gets an agreement by its id.

        Args:
            agreement_id: The id of the agreement.

        Returns:
            An agreement with the specified id.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.get(f"{self._controller}/{agreement_id}")
        raise_for_status(response)
        return ContractAgreementDTO.model_validate(response.json())


    def get_negotiation_by_agreement_id(self, agreement_id: str) -> ContractNegotiationDTO:
        """Gets a negotiation by the agreement id.

        Args:
            agreement_id: The id of the agreement.

        Returns:
            A negotiation with the specified id.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.get(f"{self._controller}/{agreement_id}/negotiation")
        raise_for_status(response)
        return ContractNegotiationDTO.model_validate(response.json())