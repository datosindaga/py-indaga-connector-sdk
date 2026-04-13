from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from dataspace_sdk.model.common import CriterionDTO

class ContractState(str, Enum):
    PREPARING = "PREPARING"
    UNDER_REVIEW = "UNDER_REVIEW"
    READY = "READY"
    PUBLISHED = "PUBLISHED"

class ContractDefinitionInputDTO(BaseModel):

    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    access_policy_id: str | None = Field(None, alias="accessPolicyId")
    contract_policy_id: str | None = Field(None, alias="contractPolicyId")
    assets_selector: list[CriterionDTO] = Field(default_factory=list, alias="assetsSelector")
    private_properties: dict[str, Any] = Field(default_factory=dict, alias="privateProperties")

    model_config = {"populate_by_name": True}

class ContractDefinitionOutputDTO(BaseModel):

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