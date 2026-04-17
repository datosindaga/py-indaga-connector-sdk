from typing import Any

from pydantic import BaseModel, Field

class PolicyDTO(BaseModel):
    """Represents an ODRL policy as embedded within a contract agreement.

    This DTO encodes the full ODRL policy that was agreed upon during contract
    negotiation. It is typically nested inside a ``ContractAgreementDTO`` rather
    than returned from a dedicated endpoint.

    Attributes:
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        id: JSON-LD identifier of the policy. Example: ``urn:uuid:6a1d3f2e-...``
        type: JSON-LD type, typically ``odrl:Agreement``.
        action: List of ODRL action objects applicable across the policy.
        permission: List of ODRL permission rules granted by this policy.
        prohibition: List of ODRL prohibition rules imposed by this policy.
        obligation: List of ODRL obligation rules required by this policy.
    """
    context: dict | list | None = Field(None, alias="@context")
    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    action: list[dict[str, Any]] = Field(default_factory=list)
    permission: list[dict[str, Any]] = Field(default_factory=list)
    prohibition: list[dict[str, Any]] = Field(default_factory=list)
    obligation: list[dict[str, Any]] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


class ContractAgreementDTO(BaseModel):
    """Represents a contract agreement as returned by the dataspace connector.

    This DTO maps to the response body of contract agreement query and fetch endpoints.
    A contract agreement is the binding result of a successfully completed contract
    negotiation and authorizes one or more data transfers between the two parties.

    Attributes:
        id: JSON-LD identifier of the contract agreement. Example: ``urn:uuid:2e9b4c7f-...``
        type: JSON-LD type, typically ``ContractAgreement``.
        asset_id: Identifier of the asset covered by this agreement.
        consumer_id: Participant identifier of the consuming connector.
        provider_id: Participant identifier of the providing connector.
        contract_signing_date: Unix epoch timestamp (ms) of when the agreement was signed.
        policy: The ODRL agreement policy that was negotiated and accepted by both parties.
    """
    context: dict | list | None = Field(None, alias="@context")
    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    asset_id: str | None = Field(None, alias="assetId")
    consumer_id: str | None = Field(None, alias="consumerId")
    provider_id: str | None = Field(None, alias="providerId")
    contract_signing_date: int | None = Field(None, alias="contractSigningDate")
    policy: PolicyDTO | None = None

    model_config = {"populate_by_name": True}