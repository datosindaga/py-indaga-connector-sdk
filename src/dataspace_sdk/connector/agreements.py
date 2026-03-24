import httpx

from dataspace_sdk.model.common import QuerySpecDTO
from dataspace_sdk.model.contractagreement import ContractAgreementDTO
from dataspace_sdk.model.contractnegotiation import ContractNegotiationDTO

class AgreementsClient:
    _controller = "/v1/contractagreements"

    def __init__(self, client: httpx.Client):
        self._client = client

    def request(self, query: QuerySpecDTO) -> list[ContractAgreementDTO]:
        response = self._client.post(
            f"{self._controller}/request",
            json=query.model_dump(by_alias=True),
        )
        return [ContractAgreementDTO.model_validate(item) for item in response.json()]


    def get_by_id(self, agreement_id: str) -> ContractAgreementDTO:
        response = self._client.get(f"{self._controller}/{agreement_id}")
        return ContractAgreementDTO.model_validate(response.json())


    def get_negotiation_by_agreement_id(self, agreement_id: str) -> ContractNegotiationDTO:
        response = self._client.get(f"{self._controller}/{agreement_id}/negotiation")
        return ContractNegotiationDTO.model_validate(response.json())