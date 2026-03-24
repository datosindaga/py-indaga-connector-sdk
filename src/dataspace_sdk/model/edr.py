from pydantic import BaseModel, Field


class EndpointDataReferenceDTO(BaseModel):

    context: dict | list | None = Field(None, alias="@context")
    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    transfer_process_id: str | None = Field(None, alias="transferProcessId")
    agreement_id: str | None = Field(None, alias="agreementId")
    contract_negotiation_id: str | None = Field(None, alias="contractNegotiationId")
    asset_id: str | None = Field(None, alias="assetId")
    provider_id: str | None = Field(None, alias="providerId")
    created_at: int | None = Field(None, alias="createdAt")

    model_config = {"populate_by_name": True}
