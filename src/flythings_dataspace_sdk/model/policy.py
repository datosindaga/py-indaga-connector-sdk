from typing import Any
from pydantic import BaseModel, Field


class PolicyDefinitionInputDTO(BaseModel):
    """Represents the input payload for creating or updating a policy definition.

    This DTO is sent as the request body to POST or PUT policy definition endpoints.
    Fields are serialized using JSON-LD conventions — use ``model_dump(by_alias=True)``
    when building the request payload.

    Attributes:
        id: JSON-LD identifier of the policy definition. Example: ``urn:uuid:7f3c2a1b-...``
        type: JSON-LD type, typically ``PolicyDefinition``.
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        policy: ODRL policy object describing permissions, prohibitions, and obligations.
        private_properties: Private metadata attached to the policy, not shared externally.
    """
    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    policy: dict[str, Any] = Field(default_factory=dict)
    private_properties: dict[str, Any] = Field(default_factory=dict, alias="privateProperties")

    model_config = {"populate_by_name": True}


class PolicyDefinitionOutputDTO(BaseModel):
    """Represents a policy definition as returned by the dataspace connector.

    This DTO maps to the response body of policy definition query and fetch endpoints.
    Fields are deserialized from JSON-LD — use ``model_validate`` with aliased keys
    when parsing connector responses.

    Attributes:
        id: JSON-LD identifier of the policy definition. Example: ``urn:uuid:7f3c2a1b-...``
        type: JSON-LD type, typically ``PolicyDefinition``.
        context: JSON-LD context as a vocabulary object.
        policy: ODRL policy object describing permissions, prohibitions, and obligations.
        private_properties: Private metadata attached to the policy, not shared externally.
    """
    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    context: dict[str, Any] = Field(default_factory=dict, alias="@context")
    policy: dict[str, Any] = Field(default_factory=dict)
    private_properties: dict[str, Any] = Field(default_factory=dict, alias="privateProperties")

    model_config = {"populate_by_name": True}


class PolicyEvaluationPlanDTO(BaseModel):
    """Represents the evaluation plan produced by the connector for a given policy.

    This DTO maps to the response body of the policy evaluation plan endpoint.
    It describes the ordered sequence of validation and rule-evaluation steps the
    connector would execute when enforcing the policy.

    Attributes:
        type: JSON-LD type, typically ``PolicyEvaluationPlan``.
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        pre_validators: Validation steps executed before rule evaluation.
        permission_steps: Evaluation steps for ODRL permission rules, keyed by rule identifier.
        prohibition_steps: Ordered evaluation steps for ODRL prohibition rules.
        obligation_steps: Ordered evaluation steps for ODRL obligation rules.
        post_validators: Validation steps executed after rule evaluation.
    """
    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    pre_validators: Any = Field(None, alias="preValidators")
    permission_steps: Any = Field(None, alias="permissionSteps")
    prohibition_steps: Any = Field(None, alias="prohibitionSteps")
    obligation_steps: Any = Field(None, alias="obligationSteps")
    post_validators: Any = Field(None, alias="postValidators")

    model_config = {"populate_by_name": True}


class PolicyEvaluationPlanRequestDTO(BaseModel):
    """Represents the input payload for requesting a policy evaluation plan.

    This DTO is sent as the request body to the policy evaluation plan endpoint.
    Fields are serialized using JSON-LD conventions — use ``model_dump(by_alias=True)``
    when building the request payload.

    Attributes:
        type: JSON-LD type, typically ``PolicyEvaluationPlanRequest``.
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        policy_scope: The scope identifier within which the policy should be evaluated,
            e.g. ``catalog`` or ``contract.negotiation``.
    """
    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    policy_scope: str | None = Field(None, alias="policyScope")

    model_config = {"populate_by_name": True}


class PolicyValidationResultDTO(BaseModel):
    """Represents the result of a policy validation check performed by the connector.

    This DTO maps to the response body of policy validation endpoints. It indicates
    whether the submitted policy is structurally and semantically valid, and surfaces
    any issues found during validation.

    Attributes:
        type: JSON-LD type, typically ``PolicyValidationResult``.
        context: JSON-LD context as a vocabulary object.
        is_valid: ``True`` if the policy passed all validation checks, ``False`` otherwise.
        errors: List of human-readable error messages describing validation failures.
            Empty when ``is_valid`` is ``True``.
    """
    type: str | None = Field(None, alias="@type")
    context: dict[str, Any] = Field(default_factory=dict, alias="@context")
    is_valid: bool | None = Field(None, alias="isValid")
    errors: list[str] = Field(default_factory=list)

    model_config = {"populate_by_name": True}