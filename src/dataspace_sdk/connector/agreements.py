from dataspace_sdk.auth.client import DataspaceClient
from dataspace_sdk.model.common import QuerySpecDTO
from dataspace_sdk.model.contractagreement import ContractAgreementDTO
from dataspace_sdk.model.contractnegotiation import ContractNegotiationDTO

CONTROLLER = "/v1/contractagreements"

def request(client: DataspaceClient, query: QuerySpecDTO) -> list[ContractAgreementDTO]:
    response = client.post(
        f"{CONTROLLER}/request",
        json=query.model_dump(by_alias=True),
    )
    return [ContractAgreementDTO.model_validate(item) for item in response.json()]


def get_by_id(client: DataspaceClient, id: str) -> ContractAgreementDTO:
    response = client.get(f"{CONTROLLER}/{id}")
    return ContractAgreementDTO.model_validate(response.json())


def get_negotiation_by_agreement_id(client: DataspaceClient, id: str) -> ContractNegotiationDTO:
    response = client.get(f"{CONTROLLER}/{id}/negotiation")
    return ContractNegotiationDTO.model_validate(response.json())