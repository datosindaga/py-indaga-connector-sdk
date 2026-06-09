from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, AliasChoices

from flythings_dataspace_sdk.model.common import QuerySpecDTO

class CatalogDTO(BaseModel):
    """Represents a DCAT catalog as returned by a provider's catalog endpoint.

    This DTO maps to the response body of catalog request endpoints. It describes
    the full set of datasets, distributions, and services advertised by a provider
    connector, and may nest further sub-catalogs for hierarchical catalog structures.

    Fields use ``AliasChoices`` to accept both prefixed (``dcat:``, ``dspace:``) and
    unprefixed keys during deserialization, and always serialize with their prefixed
    form via ``serialization_alias``.

    Attributes:
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        id: JSON-LD identifier of the catalog.
        type: JSON-LD type, typically ``dcat:Catalog``.
        distribution: List of DCAT distributions directly attached to the catalog.
        dataset: List of datasets advertised within this catalog.
        catalog: List of nested sub-catalogs, enabling hierarchical catalog structures.
        service: List of data services describing how catalog contents are accessible.
        participant_id: Dataspace participant identifier of the provider connector.
        asset_id: Plain ``id`` field as used in some connector responses for asset correlation.
        description: Human-readable description of the catalog.
        is_catalog: Marker indicating this resource is itself a catalog, as opposed to a dataset.
    """
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
    """Represents the input payload for requesting a provider's catalog.

    This DTO is sent as the request body to the catalog request endpoint.
    Fields are serialized using JSON-LD conventions — use ``model_dump(by_alias=True)``
    when building the request payload.

    Attributes:
        id: Optional JSON-LD identifier for this catalog request.
        type: JSON-LD type, typically ``CatalogRequest``.
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        protocol: Dataspace protocol to use, e.g. ``dataspace-protocol-http``.
        counter_party_address: DSP protocol endpoint URL of the provider connector.
        counter_party_id: Participant identifier of the provider connector.
        additional_scopes: List of additional credential scopes to present during the request.
        query_spec: Optional filtering, sorting, and pagination parameters to apply to the
            catalog response.
    """
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
    """Represents a DCAT data service describing an access endpoint within a catalog.

    This DTO is embedded in ``CatalogDTO.service`` and ``DistributionDTO.access_service``
    to describe how a dataset or distribution can be accessed. Fields use ``AliasChoices``
    to accept both prefixed (``dcat:``) and unprefixed keys.

    Attributes:
        id: JSON-LD identifier of the service.
        type: JSON-LD type, typically ``dcat:DataService``.
        endpoint_url: URL of the service endpoint.
        endpoint_description: Human-readable description of the endpoint.
        properties: Additional service properties not covered by declared fields.
    """
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
    """Represents an ODRL constraint expression, supporting both atomic and compound forms.

    This DTO handles the full ODRL constraint grammar. An atomic constraint is expressed
    via ``left_operand``, ``operator``, and ``right_operand``. Compound constraints are
    expressed via the logical combinators ``and_``, ``or_``, ``and_sequence``, and ``xone``,
    which may each contain nested ``ConstraintExprDTO`` instances.

    Fields use ``AliasChoices`` to accept both prefixed (``odrl:``) and unprefixed keys.

    Attributes:
        or_: List of constraint expressions of which at least one must be satisfied.
        and_sequence: List of constraint expressions that must all be satisfied in order.
        and_: List of constraint expressions that must all be satisfied.
        xone: List of constraint expressions of which exactly one must be satisfied.
        left_operand: The attribute being constrained, referenced by identifier.
        operator: The comparison operator, referenced by identifier, e.g. ``odrl:eq``.
        right_operand: The value the left operand is compared against.
    """
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
    """Represents a search request for the catalogs of the contacts.

    Attributes:
        id: Identifier of the contact or participant to look up.
        search: Free-text search string to match against contact properties.
    """
    id: str | None = None
    search: str | None = None


class DatasetDTO(BaseModel):
    """Represents a DCAT dataset entry within a provider catalog.

    This DTO maps to dataset objects nested inside a ``CatalogDTO``. It describes
    a single offered asset, including the ODRL policies under which it may be accessed
    and the distributions through which it is available. Extra fields are permitted
    to accommodate connector-specific dataset metadata.

    Fields use ``AliasChoices`` to accept both prefixed (``dcat:``, ``odrl:``) and
    unprefixed keys.

    Attributes:
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        type: JSON-LD type, typically ``dcat:Dataset``.
        id: JSON-LD identifier of the dataset, corresponding to the asset identifier.
        distribution: List of DCAT distributions describing access options for this dataset.
        has_policy: List of ODRL offer policies governing access to this dataset.
    """
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
    """Represents the input payload for requesting a single dataset from a provider catalog.

    This DTO is sent as the request body to the dataset fetch endpoint. It identifies
    the target provider and the specific dataset to retrieve.
    Fields are serialized using JSON-LD conventions — use ``model_dump(by_alias=True)``
    when building the request payload.

    Attributes:
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        type: JSON-LD type, typically ``DatasetRequest``.
        id: JSON-LD identifier of the dataset (asset) to retrieve.
        protocol: Dataspace protocol to use, e.g. ``dataspace-protocol-http``.
        counter_party_address: DSP protocol endpoint URL of the provider connector.
        counter_party_id: Participant identifier of the provider connector.
        query_spec: Optional filtering and pagination parameters for the dataset response.
    """
    context: dict | list | None = Field(None, alias="@context")
    type: str | None = Field(None, alias="@type")
    id: str | None = Field(None, alias="@id")
    protocol: str | None = None
    counter_party_address: str | None = Field(None, alias="counterPartyAddress")
    counter_party_id: str | None = Field(None, alias="counterPartyId")
    query_spec: QuerySpecDTO | None = Field(None, alias="querySpec")

    model_config = {"populate_by_name": True}


class DetailedDatasetDTO(BaseModel):
    """Represents a dataset entry with additional provider context.

    Extends the base ``DatasetDTO`` representation with a ``provider`` field for use
    in contexts where the originating provider must be tracked alongside the dataset,
    such as in aggregated or federated catalog views. Extra fields are permitted to
    accommodate connector-specific dataset metadata.

    Attributes:
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        type: JSON-LD type, typically ``dcat:Dataset``.
        id: JSON-LD identifier of the dataset, corresponding to the asset identifier.
        distribution: List of DCAT distributions describing access options for this dataset.
        has_policy: List of ODRL offer policies governing access to this dataset.
        provider: Participant identifier or endpoint URL of the provider that advertised
            this dataset.
    """
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
    """Represents a DCAT distribution describing one concrete access option for a dataset.

    This DTO is embedded in ``DatasetDTO.distribution`` and ``CatalogDTO.distribution``.
    Each distribution pairs a transfer format with the service endpoint through which
    it is accessible, along with the policies that govern access.

    Fields use ``AliasChoices`` to accept both prefixed (``dcat:``, ``odrl:``, ``dct:``)
    and unprefixed keys.

    Attributes:
        type: JSON-LD type, typically ``dcat:Distribution``.
        has_policy: List of ODRL offer policies governing access via this distribution.
        access_service: The data service through which this distribution is accessible.
        format: The transfer format of this distribution, e.g. ``HttpData-PULL``.
    """
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
    """Represents an ODRL offer policy attached to a catalog dataset or distribution.

    This DTO encodes the policy under which a provider offers access to an asset,
    as advertised in the catalog. It is embedded in ``DatasetDTO.has_policy`` and
    ``DistributionDTO.has_policy``, and its ``id`` is used as the policy identifier
    when constructing a ``ContractRequestDTO``.

    Fields use ``AliasChoices`` to accept both prefixed (``odrl:``) and unprefixed keys.

    Attributes:
        id: JSON-LD identifier of the offer policy.
        type: JSON-LD type, typically ``odrl:Offer``.
        profile: List of ODRL profile URIs this policy conforms to.
        permission: List of ODRL permission rules granted by this offer.
        prohibition: List of ODRL prohibition rules imposed by this offer.
        obligation: List of ODRL obligation rules required by this offer.
    """
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
    """Represents a single ODRL policy rule (permission, prohibition, or obligation).

    This DTO is embedded in ``OfferPolicyDTO`` and encodes one rule within an ODRL
    policy, pairing an action with the constraints under which that action applies.

    Fields use ``AliasChoices`` to accept both prefixed (``odrl:``) and unprefixed keys.

    Attributes:
        action: The ODRL action this rule governs, referenced by identifier,
            e.g. ``odrl:use``.
        constraint: List of constraints that must hold for this rule to apply.
    """
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
    """Represents a JSON-LD term reference, wrapping an IRI as an ``@id`` node.

    Used throughout catalog and policy DTOs wherever ODRL or DCAT terms reference
    other resources by identifier rather than embedding them inline — for example,
    actions, operators, and format identifiers.

    Attributes:
        id: The IRI of the referenced term. Example: ``odrl:use``, ``dct:format``.
    """
    id: str = Field(alias="@id")

    model_config = {"populate_by_name": True}

# Resolve forward references between DTOs defined in this module.
for _model in (
        CatalogDTO,
        CatalogServiceDTO,
        ConstraintExprDTO,
        DatasetDTO,
        DetailedDatasetDTO,
        DistributionDTO,
        OfferPolicyDTO,
        PolicyRuleDTO,
        TermRef,
):
    _model.model_rebuild()