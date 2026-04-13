from typing import Any

from pydantic import BaseModel, Field, AliasChoices

from dataspace_sdk.model.common import QuerySpecDTO

class CatalogDTO(BaseModel):

    context: dict | list | None = Field(None, alias="@context")
    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    distribution: list[DistributionDTO] = Field(
        default_factory=list,
        validation_alias=AliasChoices("dcat:distribution", "distribution"),
        serialization_alias="dcat:distribution",
    )
    dataset: list[DatasetDTO] = Field(
        default_factory=list,
        validation_alias=AliasChoices("dcat:dataset", "dataset"),
        serialization_alias="dcat:dataset",
    )
    catalog: list[CatalogDTO] = Field(
        default_factory=list,
        validation_alias=AliasChoices("dcat:catalog", "catalog"),
        serialization_alias="dcat:catalog",
    )
    service: list[CatalogServiceDTO] = Field(
        default_factory=list,
        validation_alias=AliasChoices("dcat:service", "service"),
        serialization_alias="dcat:service",
    )
    participant_id: str | None = Field(
        None,
        validation_alias=AliasChoices("dspace:participantId", "participantId"),
        serialization_alias="dspace:participantId",
    )
    asset_id: str | None = Field(None, alias="id")
    description: str | None = None
    is_catalog: str | None = Field(None, alias="isCatalog")

    model_config = {"populate_by_name": True}

class CatalogRequestDTO(BaseModel):

    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    protocol: str | None = None
    counter_party_address: str | None = Field(None, alias="counterPartyAddress")
    counter_party_id: str | None = Field(None, alias="counterPartyId")
    additional_scopes: list[str] = Field(default_factory=list, alias="additionalScopes")
    query_spec: QuerySpecDTO | None = Field(None, alias="querySpec")

    model_config = {"populate_by_name": True}

class CatalogServiceDTO(BaseModel):

    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    endpoint_url: str | None = Field(
        None,
        validation_alias=AliasChoices("dcat:endpointURL", "endpointUrl"),
        serialization_alias="dcat:endpointURL",
    )
    endpoint_description: str | None = Field(
        None,
        validation_alias=AliasChoices("dcat:endpointDescription", "endpointDescription"),
        serialization_alias="dcat:endpointDescription",
    )
    properties: dict[str, Any] = Field(default_factory=dict)

    model_config = {"populate_by_name": True}

class ConstraintExprDTO(BaseModel):

    or_: list[Any] = Field(default_factory=list, alias="or")
    and_sequence: list[Any] = Field(default_factory=list, alias="andSequence")
    and_: list[Any] = Field(default_factory=list, alias="and")
    xone: list[Any] = Field(default_factory=list)

    left_operand: TermRef | None = Field(
        None,
        validation_alias=AliasChoices("odrl:leftOperand", "leftOperand"),
        serialization_alias="odrl:leftOperand",
    )
    operator: TermRef | None = Field(
        None,
        validation_alias=AliasChoices("odrl:operator", "operator"),
        serialization_alias="odrl:operator",
    )
    right_operand: Any = Field(
        None,
        validation_alias=AliasChoices("odrl:rightOperand", "rightOperand"),
        serialization_alias="odrl:rightOperand",
    )

    model_config = {"populate_by_name": True}

class ContactRequestDTO(BaseModel):

    id: str | None = None
    search: str | None = None

class DatasetDTO(BaseModel):

    context: dict | list | None = Field(None, alias="@context")
    type: str | None = Field(None, alias="@type")
    id: str | None = Field(None, alias="@id")
    distribution: list[DistributionDTO] = Field(
        default_factory=list,
        validation_alias=AliasChoices("dcat:distribution", "distribution"),
        serialization_alias="dcat:distribution",
    )
    has_policy: list[OfferPolicyDTO] = Field(
        default_factory=list,
        validation_alias=AliasChoices("odrl:hasPolicy", "hasPolicy"),
        serialization_alias="odrl:hasPolicy",
    )

    model_config = {"populate_by_name": True, "extra": "allow"}

class DatasetRequestDTO(BaseModel):

    context: dict | list | None = Field(None, alias="@context")
    type: str | None = Field(None, alias="@type")
    id: str | None = Field(None, alias="@id")
    protocol: str | None = None
    counter_party_address: str | None = Field(None, alias="counterPartyAddress")
    counter_party_id: str | None = Field(None, alias="counterPartyId")
    query_spec: QuerySpecDTO | None = Field(None, alias="querySpec")

    model_config = {"populate_by_name": True}

class DetailedDatasetDTO(BaseModel):

    context: dict | list | None = Field(None, alias="@context")
    type: str | None = Field(None, alias="@type")
    id: str | None = Field(None, alias="@id")
    distribution: list[DistributionDTO] = Field(
        default_factory=list,
        validation_alias=AliasChoices("dcat:distribution", "distribution"),
        serialization_alias="dcat:distribution",
    )
    has_policy: list[OfferPolicyDTO] = Field(
        default_factory=list,
        validation_alias=AliasChoices("odrl:hasPolicy", "hasPolicy"),
        serialization_alias="odrl:hasPolicy",
    )
    provider: str | None = None

    model_config = {"populate_by_name": True, "extra": "allow"}

class DistributionDTO(BaseModel):

    type: str | None = Field(None, alias="@type")
    has_policy: list[OfferPolicyDTO] = Field(
        default_factory=list,
        validation_alias=AliasChoices("odrl:hasPolicy", "hasPolicy"),
        serialization_alias="odrl:hasPolicy",
    )
    access_service: CatalogServiceDTO | None = Field(
        None,
        validation_alias=AliasChoices("dcat:accessService", "accessService"),
        serialization_alias="dcat:accessService",
    )
    format: TermRef | None = Field(
        None,
        validation_alias=AliasChoices("dct:format", "format"),
        serialization_alias="dct:format",
    )

    model_config = {"populate_by_name": True}

class OfferPolicyDTO(BaseModel):

    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    profile: list[str] = Field(default_factory=list)
    permission: list[PolicyRuleDTO] = Field(
        default_factory=list,
        validation_alias=AliasChoices("odrl:permission", "permission"),
        serialization_alias="odrl:permission",
    )
    prohibition: list[PolicyRuleDTO] = Field(
        default_factory=list,
        validation_alias=AliasChoices("odrl:prohibition", "prohibition"),
        serialization_alias="odrl:prohibition",
    )
    obligation: list[PolicyRuleDTO] = Field(
        default_factory=list,
        validation_alias=AliasChoices("odrl:obligation", "obligation"),
        serialization_alias="odrl:obligation",
    )

    model_config = {"populate_by_name": True}

class PolicyRuleDTO(BaseModel):

    action: TermRef | None = Field(
        None,
        validation_alias=AliasChoices("odrl:action", "action"),
        serialization_alias="odrl:action",
    )
    constraint: list[ConstraintExprDTO] = Field(
        default_factory=list,
        validation_alias=AliasChoices("odrl:constraint", "constraint"),
        serialization_alias="odrl:constraint",
    )

    model_config = {"populate_by_name": True}

class TermRef(BaseModel):
    id: str = Field(alias="@id")

    model_config = {"populate_by_name": True}