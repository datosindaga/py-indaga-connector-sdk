import httpx

from model.common import QuerySpecDTO
from model.contractagreement import ContractAgreementDTO
from model.contractnegotiation import ContractNegotiationDTO

class ContractAgreementsClient:
    _controller = "/v1/contractagreements"

    def __init__(self, client: httpx.Client):
        self._client = client

    def request(self, query: QuerySpecDTO) -> list[ContractAgreementDTO]:
        """Retrieves a paginated list of assets matching the given query criteria.

        Args:
            query: The query specification defining filters, pagination, and sorting.

        Returns:
            A list of assets matching the criteria. Empty list if none found.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            f"{self._controller}/request",
            json=query.model_dump(by_alias=True),
        )
        return [ContractAgreementDTO.model_validate(item) for item in response.json()]


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
        return ContractNegotiationDTO.model_validate(response.json())