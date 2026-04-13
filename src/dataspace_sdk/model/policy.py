from typing import Any
from pydantic import BaseModel, Field


class PolicyDefinitionInputDTO(BaseModel):

    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    policy: dict[str, Any] = Field(default_factory=dict)
    private_properties: dict[str, Any] = Field(default_factory=dict, alias="privateProperties")

    model_config = {"populate_by_name": True}


class PolicyDefinitionOutputDTO(BaseModel):

    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    context: dict[str, Any] = Field(default_factory=dict, alias="@context")
    policy: dict[str, Any] = Field(default_factory=dict)
    private_properties: dict[str, Any] = Field(default_factory=dict, alias="privateProperties")

    model_config = {"populate_by_name": True}


class PolicyEvaluationPlanDTO(BaseModel):

    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    pre_validators: Any = Field(None, alias="preValidators")
    permission_steps: dict[str, Any] = Field(default_factory=dict, alias="permissionSteps")
    prohibition_steps: list[dict[str, Any]] = Field(default_factory=list, alias="prohibitionSteps")
    obligation_steps: list[dict[str, Any]] = Field(default_factory=list, alias="obligationSteps")
    post_validators: Any = Field(None, alias="postValidators")

    model_config = {"populate_by_name": True}


class PolicyEvaluationPlanRequestDTO(BaseModel):

    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    policy_scope: str | None = Field(None, alias="policyScope")

    model_config = {"populate_by_name": True}


class PolicyValidationResultDTO(BaseModel):

    type: str | None = Field(None, alias="@type")
    context: dict[str, Any] = Field(default_factory=dict, alias="@context")
    is_valid: bool | None = Field(None, alias="isValid")
    errors: list[str] = Field(default_factory=list)

    model_config = {"populate_by_name": True}