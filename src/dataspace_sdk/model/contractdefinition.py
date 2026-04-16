from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from dataspace_sdk.model.common import CriterionDTO

class ContractState(str, Enum):
    """Enumerates the possible lifecycle states of a contract definition.

    Attributes:
        PREPARING: The contract definition is being configured and is not yet active.
        UNDER_REVIEW: The contract definition is undergoing review before publication.
        READY: The contract definition has been validated and is ready to be published.
        PUBLISHED: The contract definition is active and visible in the provider's catalog.
    """
    PREPARING = "PREPARING"
    UNDER_REVIEW = "UNDER_REVIEW"
    READY = "READY"
    PUBLISHED = "PUBLISHED"


class ContractDefinitionInputDTO(BaseModel):
    """Represents the input payload for creating or updating a contract definition.

    This DTO is sent as the request body to POST or PUT contract definition endpoints.
    Fields are serialized using JSON-LD conventions — use ``model_dump(by_alias=True)``
    when building the request payload.

    Attributes:
        id: JSON-LD identifier of the contract definition. Example: ``urn:uuid:9c4e2b1a-...``
        type: JSON-LD type, typically ``ContractDefinition``.
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        access_policy_id: Identifier of the policy that governs who may see this contract
            in the catalog.
        contract_policy_id: Identifier of the policy that governs the terms under which
            data may be transferred.
        assets_selector: List of criteria used to select which assets this contract
            definition applies to.
        private_properties: Private metadata attached to the contract definition,
            not shared externally.
    """
    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    access_policy_id: str | None = Field(None, alias="accessPolicyId")
    contract_policy_id: str | None = Field(None, alias="contractPolicyId")
    assets_selector: list[CriterionDTO] = Field(default_factory=list, alias="assetsSelector")
    private_properties: dict[str, Any] = Field(default_factory=dict, alias="privateProperties")

    model_config = {"populate_by_name": True}


class ContractDefinitionOutputDTO(BaseModel):
    """Represents a contract definition as returned by the dataspace connector.

    This DTO maps to the response body of contract definition query and fetch endpoints.
    Fields are deserialized from JSON-LD — use ``model_validate`` with aliased keys
    when parsing connector responses.

    Attributes:
        id: JSON-LD identifier of the contract definition. Example: ``urn:uuid:9c4e2b1a-...``
        type: JSON-LD type, typically ``ContractDefinition``.
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        access_policy_id: Identifier of the policy that governs who may see this contract
            in the catalog.
        contract_policy_id: Identifier of the policy that governs the terms under which
            data may be transferred.
        assets_selector: List of criteria used to select which assets this contract
            definition applies to.
        private_properties: Private metadata attached to the contract definition,
            not shared externally.
        state: Current lifecycle state of the contract definition.
        created_at: Unix epoch timestamp (ms) of when the contract definition was created.
    """
    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    access_policy_id: str | None = Field(None, alias="accessPolicyId")
    contract_policy_id: str | None = Field(None, alias="contractPolicyId")
    assets_selector: list[CriterionDTO] = Field(default_factory=list, alias="assetsSelector")
    private_properties: dict[str, Any] = Field(default_factory=dict, alias="privateProperties")
    state: ContractState | None = None
    created_at: int | None = Field(None, alias="createdAt")

    model_config = {"populate_by_name": True}