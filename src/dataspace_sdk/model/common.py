from enum import Enum

from pydantic import BaseModel, Field
from typing import Any


class IdResponseDTO(BaseModel):
    """Represents a minimal identifier response returned after a successful write operation.

    This DTO maps to the response body of POST and PUT endpoints that confirm
    creation or update of a resource by echoing back its JSON-LD identifier and type.

    Attributes:
        id: JSON-LD identifier of the created or updated resource. Example: ``urn:uuid:1a2b3c4d-...``
        type: JSON-LD type of the resource, e.g. ``Asset``, ``PolicyDefinition``.
    """
    id: str = Field(alias="@id")
    type: str = Field(alias="@type")

    model_config = {"populate_by_name": True}


class CriterionDTO(BaseModel):
    """Represents a single filter criterion used in query expressions and asset selectors.

    This DTO is used both in ``QuerySpecDTO.filter_expression`` for querying resources
    and in ``ContractDefinitionInputDTO.assets_selector`` for matching assets to contract
    definitions.

    Attributes:
        type: JSON-LD type, typically ``Criterion``.
        operand_left: The property path to filter on, e.g. ``'https://w3id.org/edc/v0.0.1/ns/id'``.
        operand_right: The value to compare against. May be a scalar or a list depending on
            the operator.
        operator: Comparison operator, e.g. ``=``, ``in``, ``like``.
    """
    type: str | None = Field(None, alias="@type")
    operand_left: str = Field(alias="operandLeft")
    operand_right: Any = Field(alias="operandRight")
    operator: str

    model_config = {"populate_by_name": True}


class CallbackAddressDTO(BaseModel):
    """Represents a webhook endpoint to be notified on dataspace process state changes.

    This DTO is embedded in transfer process and contract negotiation request payloads
    to register callbacks that the connector will invoke as the process transitions
    between lifecycle states.

    Attributes:
        type: JSON-LD type, typically ``CallbackAddress``.
        auth_code_id: Vault alias of the secret used as the authentication credential value.
        auth_key: HTTP header name to use when sending the authentication credential,
            e.g. ``Authorization``.
        events: List of event type URIs that should trigger this callback,
            e.g. ``transfer.process.started``.
        transactional: If ``True``, the callback is invoked within the process transaction
            and failures will roll back the state transition.
        uri: HTTP endpoint URL to deliver the callback notification to.
    """
    type: str | None = Field(None, alias="@type")
    auth_code_id: str | None = Field(None, alias="authCodeId")
    auth_key: str | None = Field(None, alias="authKey")
    events: list[str] = Field(default_factory=list)
    transactional: bool | None = None
    uri: str | None = None

    model_config = {"populate_by_name": True}


class DataAddressDTO(BaseModel):
    """Represents the address and access configuration of a data source or destination.

    This DTO is embedded in asset definitions to describe where asset data is located,
    and in transfer requests and process responses to describe the data delivery endpoint.
    Extra fields beyond those declared are permitted to accommodate connector-specific
    address properties.

    Attributes:
        type: JSON-LD type, typically ``DataAddress``.
        address_type: The transport type of this address, e.g. ``HttpData``, ``AmazonS3``.
        base_url: Base URL of the data source or destination endpoint.
        proxy_path: If ``True``, the connector will forward path segments appended by the consumer.
        proxy_query_params: If ``True``, the connector will forward query parameters from the consumer.
        endpoint: Fully resolved endpoint URL, typically populated in EDR responses.
        authorization: Bearer token or other credential for accessing the endpoint,
            typically populated in EDR responses.
    """
    type: str | None = Field(None, alias="@type")
    address_type: str | None = Field(None, alias="type")
    base_url: str | None = Field(None, alias="baseUrl")
    proxy_path: bool | None = Field(None, alias="proxyPath")
    proxy_query_params: bool | None = Field(None, alias="proxyQueryParams")
    endpoint: str | None = None
    authorization: str | None = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class SortOrder(str, Enum):
    """Specifies the sort direction for paginated query results.

    Attributes:
        ASC: Sort results in ascending order.
        DESC: Sort results in descending order.
    """
    ASC = "ASC"
    DESC = "DESC"


class QuerySpecDTO(BaseModel):
    """Represents the input payload for querying and paginating connector resources.

    This DTO is sent as the request body to POST query endpoints across all resource
    types (assets, policies, contract definitions, negotiations, transfer processes).
    Fields are serialized using JSON-LD conventions — use ``model_dump(by_alias=True)``
    when building the request payload.

    Attributes:
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        type: JSON-LD type, typically ``QuerySpec``.
        offset: Zero-based index of the first result to return.
        limit: Maximum number of results to return.
        sort_field: Property path to sort results by, e.g. ``'https://w3id.org/edc/v0.0.1/ns/id'``.
        sort_order: Direction to sort results, either ``ASC`` or ``DESC``.
        filter_expression: List of criteria to filter results by. Multiple criteria are
            combined with a logical AND.
    """
    context: dict | list | None = Field(None, alias="@context")
    type: str | None = Field(None, alias="@type")
    offset: int | None = None
    limit: int | None = None
    sort_field: str | None = Field(None, alias="sortField")
    sort_order: SortOrder | None = Field(None, alias="sortOrder")
    filter_expression: list[CriterionDTO] = Field(default_factory=list, alias="filterExpression")

    model_config = {"populate_by_name": True}