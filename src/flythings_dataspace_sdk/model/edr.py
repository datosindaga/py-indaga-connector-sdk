from pydantic import BaseModel, Field

class EndpointDataReferenceDTO(BaseModel):
    """Represents an endpoint data reference issued upon a successful data transfer.

    This DTO maps to the response body returned when querying EDRs associated with
    a transfer process. It carries the identifiers needed to locate and authorize
    access to the data endpoint provisioned by the provider.

    Attributes:
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        id: JSON-LD identifier of the endpoint data reference.
        type: JSON-LD type, typically ``EndpointDataReference``.
        transfer_process_id: Identifier of the transfer process that produced this EDR.
        agreement_id: Identifier of the contract agreement under which the transfer was authorized.
        contract_negotiation_id: Identifier of the contract negotiation that led to the agreement.
        asset_id: Identifier of the asset being made accessible via this endpoint reference.
        provider_id: Identifier of the provider connector that issued this EDR.
        created_at: Unix epoch timestamp (ms) of when the EDR was created.
    """
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
