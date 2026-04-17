from typing import Any
from pydantic import BaseModel, Field

from model.common import CallbackAddressDTO


class ContractNegotiationDTO(BaseModel):
    """Represents a contract negotiation as returned by the dataspace connector.

    This DTO maps to the response body of contract negotiation query and fetch endpoints.
    Fields are deserialized from JSON-LD — use ``model_validate`` with aliased keys
    when parsing connector responses.

    Attributes:
        id: JSON-LD identifier of the contract negotiation. Example: ``urn:uuid:4d2f1a9c-...``
        type: JSON-LD type, typically ``ContractNegotiation``.
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        callback_addresses: List of callback endpoints notified on negotiation state changes.
        contract_agreement_id: Identifier of the resulting contract agreement, populated once
            the negotiation reaches ``AGREED`` state.
        counter_party_address: DSP protocol endpoint URL of the counterparty connector.
        counter_party_id: Participant identifier of the counterparty connector.
        error_detail: Human-readable error description, populated when negotiation fails.
        protocol: Dataspace protocol used for this negotiation, e.g. ``dataspace-protocol-http``.
        state: Current lifecycle state of the negotiation, e.g. ``REQUESTED``, ``AGREED``, ``FINALIZED``.
        type_role: Whether the local connector is acting as ``CONSUMER`` or ``PROVIDER``.
        asset_id: Identifier of the asset targeted by this negotiation.
        private_properties: Private metadata attached to the negotiation, not shared externally.
        created_at: Unix epoch timestamp (ms) of when the negotiation was created.
    """
    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    callback_addresses: list[CallbackAddressDTO] = Field(default_factory=list, alias="callbackAddresses")
    contract_agreement_id: str | None = Field(None, alias="contractAgreementId")
    counter_party_address: str | None = Field(None, alias="counterPartyAddress")
    counter_party_id: str | None = Field(None, alias="counterPartyId")
    error_detail: str | None = Field(None, alias="errorDetail")
    protocol: str | None = None
    state: str | None = None
    type_role: str | None = Field(None, alias="type")
    asset_id: str | None = Field(None, alias="assetId")
    private_properties: dict[str, Any] = Field(default_factory=dict, alias="privateProperties")
    created_at: int | None = Field(None, alias="createdAt")

    model_config = {"populate_by_name": True}


class OfferDTO(BaseModel):
    """Represents an ODRL offer policy attached to a contract negotiation request.

    This DTO encodes the ODRL offer that the consumer proposes to the provider
    during contract negotiation. It is embedded within ``ContractRequestDTO``
    rather than sent to a dedicated endpoint.

    Attributes:
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        type: JSON-LD type, typically ``Offer``.
        id: JSON-LD identifier of the offer, typically matching the catalog policy identifier.
        assigner: Participant identifier of the policy assigner (the provider).
        target: Identifier of the asset this offer applies to.
        permission: List of ODRL permission rules granted by this offer.
        prohibition: List of ODRL prohibition rules imposed by this offer.
        obligation: List of ODRL obligation rules required by this offer.
    """
    context: dict | list | None = Field(None, alias="@context")
    type: str | None = Field(None, alias="@type")
    id: str | None = Field(None, alias="@id")
    assigner: str | None = None
    target: str | None = None
    permission: list[dict[str, Any]] = Field(default_factory=list)
    prohibition: list[dict[str, Any]] = Field(default_factory=list)
    obligation: list[dict[str, Any]] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


class ContractRequestDTO(BaseModel):
    """Represents the input payload for initiating a contract negotiation.

    This DTO is sent as the request body to the contract negotiation initiation endpoint.
    Fields are serialized using JSON-LD conventions — use ``model_dump(by_alias=True)``
    when building the request payload.

    Attributes:
        type: JSON-LD type, typically ``ContractRequest``.
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        callback_addresses: List of callback endpoints to be notified on negotiation state changes.
        counter_party_address: DSP protocol endpoint URL of the provider connector.
        policy: ODRL offer to propose to the provider, including permissions and target asset.
        protocol: Dataspace protocol to use, e.g. ``dataspace-protocol-http``.
        private_properties: Private metadata attached to the negotiation, not shared externally.
    """
    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    callback_addresses: list[CallbackAddressDTO] = Field(default_factory=list, alias="callbackAddresses")
    counter_party_address: str | None = Field(None, alias="counterPartyAddress")
    policy: OfferDTO | None = None
    protocol: str | None = None
    private_properties: dict[str, Any] = Field(default_factory=dict, alias="privateProperties")

    model_config = {"populate_by_name": True}


class NegotiationStateDTO(BaseModel):
    """Represents the current state of a contract negotiation as a lightweight response body.

    This DTO is typically returned by state-query endpoints that report only the
    current lifecycle state rather than the full negotiation representation.

    Attributes:
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        state: Current lifecycle state of the negotiation, e.g. ``REQUESTED``, ``AGREED``, ``FINALIZED``.
    """
    context: dict | list | None = Field(None, alias="@context")
    state: str | None = None

    model_config = {"populate_by_name": True}


class TerminationNegotiationDTO(BaseModel):
    """Represents the input payload for terminating an in-progress contract negotiation.

    This DTO is sent as the request body to the contract negotiation termination endpoint.
    Fields are serialized using JSON-LD conventions — use ``model_dump(by_alias=True)``
    when building the request payload.

    Attributes:
        id: JSON-LD identifier of the contract negotiation to terminate.
        type: JSON-LD type, typically ``TerminationNegotiation``.
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        reason: Human-readable explanation of why the negotiation is being terminated.
    """
    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    reason: str | None = None

    model_config = {"populate_by_name": True}