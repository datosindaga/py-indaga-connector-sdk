from enum import Enum

from pydantic import BaseModel, BeforeValidator, Field
from typing import Annotated, Any, Generic, TypeVar, Union

T = TypeVar("T")


class PaginatedResultDTO(BaseModel, Generic[T]):
    """Paginated response wrapper returned by /request endpoints.

    Attributes:
        items: Items returned in the current response.
        has_more: Whether more items are available after this response.
    """
    items: list[T]
    has_more: bool | None = Field(None, alias="hasMore")

    model_config = {"populate_by_name": True}


class IdResponseDTO(BaseModel):
    """Represents a minimal identifier response returned after a successful write operation.

    This DTO maps to the response body of POST and PUT endpoints that confirm
    creation or update of a resource by echoing back its JSON-LD identifier and type.

    Attributes:
        id: JSON-LD identifier of the created or updated resource. Example: ``urn:uuid:1a2b3c4d-...``
        type: JSON-LD type of the resource, e.g. ``Asset``, ``PolicyDefinition``.
    """
    id: str = Field(alias="@id")
    type: str | None = Field(None, alias="@type")

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


_HTTP_ADDRESS_TYPES = frozenset({"HttpData", "https://w3id.org/idsa/v4.1/HTTP"})


class DataAddressDTO(BaseModel):
    """Generic data address, compatible with all connector address types.

    For response parsing, SDK model fields use ``AnyDataAddressDTO`` which
    automatically dispatches to the appropriate typed subclass based on the
    ``type`` discriminator. Use ``DataAddressDTO`` directly when constructing
    request payloads and no specific address type is needed.

    Attributes:
        type: JSON-LD type, typically ``DataAddress``.
        address_type: Transport type discriminator, e.g. ``HttpData``, ``AmazonS3``.
        base_url: Base URL of the data source or destination endpoint.
        proxy_path: If ``True``, connector forwards path segments from the consumer.
        proxy_query_params: If ``True``, connector forwards query parameters from the consumer.
        endpoint: Fully resolved endpoint URL, typically populated in EDR responses.
        authorization: Bearer token or credential for the endpoint.
    """
    type: str | None = Field(None, alias="@type")
    address_type: str | None = Field(None, alias="type")
    base_url: str | None = Field(None, alias="baseUrl")
    proxy_path: bool | None = Field(None, alias="proxyPath")
    proxy_query_params: bool | None = Field(None, alias="proxyQueryParams")
    endpoint: str | None = None
    authorization: str | None = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class HttpDataAddressDTO(BaseModel):
    """Data address for HTTP-based data sources and destinations.

    Used when the ``type`` discriminator is ``"HttpData"`` or
    ``"https://w3id.org/idsa/v4.1/HTTP"``.

    Attributes:
        type: JSON-LD type.
        address_type: Discriminator value, e.g. ``"HttpData"``.
        base_url: Base URL of the HTTP endpoint.
        base_path: Optional base path appended to ``base_url``.
        method: HTTP method, e.g. ``"GET"``.
        proxy_path: If ``True``, connector proxies path segments from the consumer.
        proxy_query_params: If ``True``, connector proxies query parameters from the consumer.
        endpoint: Fully resolved endpoint URL used to build the HTTP request.
        auth_key: HTTP header name for the authentication credential.
        auth_code: Vault alias for the authentication credential value.
        authorization: Value sent as the ``Authorization`` header.
        query_params: Additional query parameters.
        parameterization: Parameterization configuration.
        data_sink: Data sink configuration.
    """
    type: str | None = Field(None, alias="@type")
    address_type: str | None = Field(None, alias="type")
    base_url: str | None = Field(None, alias="baseUrl")
    base_path: str | None = Field(None, alias="basePath")
    method: str | None = None
    proxy_path: bool | None = Field(None, alias="proxyPath")
    proxy_query_params: bool | None = Field(None, alias="proxyQueryParams")
    endpoint: str | None = None
    auth_key: str | None = Field(None, alias="authKey")
    auth_code: str | None = Field(None, alias="authCode")
    authorization: str | None = None
    query_params: Any = Field(None, alias="queryParams")
    parameterization: Any = None
    data_sink: Any = Field(None, alias="dataSink")

    model_config = {"populate_by_name": True, "extra": "allow"}


class S3DataAddressDTO(BaseModel):
    """Data address for Amazon S3 data sources and destinations.

    Used when the ``type`` discriminator is ``"AmazonS3"``.

    Attributes:
        type: JSON-LD type.
        address_type: Discriminator value, ``"AmazonS3"``.
        region: AWS region of the S3 bucket.
        bucket_name: Name of the S3 bucket.
        object_name: Key of the S3 object.
        object_prefix: Prefix for S3 object keys.
        endpoint_override: Custom S3-compatible endpoint URL.
        secret_access_key: AWS secret access key.
        access_key_id: AWS access key ID.
        key_name: Vault alias for the credential.
    """
    type: str | None = Field(None, alias="@type")
    address_type: str | None = Field(None, alias="type")
    region: str | None = None
    bucket_name: str | None = Field(None, alias="bucketName")
    object_name: str | None = Field(None, alias="objectName")
    object_prefix: str | None = Field(None, alias="objectPrefix")
    endpoint_override: str | None = Field(None, alias="endpointOverride")
    secret_access_key: str | None = Field(None, alias="secretAccessKey")
    access_key_id: str | None = Field(None, alias="accessKeyId")
    key_name: str | None = Field(None, alias="keyName")

    model_config = {"populate_by_name": True, "extra": "allow"}


class AzureStorageDataAdressDTO(BaseModel):
    """Data address for Azure Blob Storage data sources and destinations.

    Used when the ``type`` discriminator is ``"AzureStorage"``.

    Note: the class name preserves the typo from the Java source (``DataAdress``).

    Attributes:
        type: JSON-LD type.
        address_type: Discriminator value, ``"AzureStorage"``.
        account: Azure storage account name.
        container: Blob container name.
        blob_name: Name of the blob.
        blob_prefix: Prefix for blob names.
        account_key: Azure storage account key.
        sas_token: Shared Access Signature token.
        endpoint: Azure storage endpoint URL.
        key_name: Vault alias for the credential.
    """
    type: str | None = Field(None, alias="@type")
    address_type: str | None = Field(None, alias="type")
    account: str | None = None
    container: str | None = None
    blob_name: str | None = Field(None, alias="blobName")
    blob_prefix: str | None = Field(None, alias="blobPrefix")
    account_key: str | None = Field(None, alias="accountKey")
    sas_token: str | None = Field(None, alias="sasToken")
    endpoint: str | None = None
    key_name: str | None = Field(None, alias="keyName")

    model_config = {"populate_by_name": True, "extra": "allow"}


class GenericDataAddressDTO(BaseModel):
    """Fallback data address for unrecognized ``type`` values.

    Captures all fields as extra attributes via ``model_extra``.

    Attributes:
        type: JSON-LD type.
        address_type: Transport type discriminator (any unrecognized value).
    """
    type: str | None = Field(None, alias="@type")
    address_type: str | None = Field(None, alias="type")

    model_config = {"populate_by_name": True, "extra": "allow"}


def _dispatch_data_address(v: Any) -> Any:
    if isinstance(v, (DataAddressDTO, HttpDataAddressDTO, S3DataAddressDTO,
                      AzureStorageDataAdressDTO, GenericDataAddressDTO)):
        return v
    if isinstance(v, dict):
        t = v.get("type")
        if t in _HTTP_ADDRESS_TYPES:
            return HttpDataAddressDTO.model_validate(v)
        if t == "AmazonS3":
            return S3DataAddressDTO.model_validate(v)
        if t == "AzureStorage":
            return AzureStorageDataAdressDTO.model_validate(v)
        return GenericDataAddressDTO.model_validate(v)
    return v


AnyDataAddressDTO = Annotated[
    Union[HttpDataAddressDTO, S3DataAddressDTO, AzureStorageDataAdressDTO, GenericDataAddressDTO, DataAddressDTO],
    BeforeValidator(_dispatch_data_address),
]
"""Polymorphic data address type for use in field annotations.

When Pydantic validates a dict through this type, it dispatches to the appropriate
typed subclass based on the ``type`` discriminator field:

- ``"HttpData"`` / ``"https://w3id.org/idsa/v4.1/HTTP"`` → ``HttpDataAddressDTO``
- ``"AmazonS3"`` → ``S3DataAddressDTO``
- ``"AzureStorage"`` → ``AzureStorageDataAdressDTO``
- anything else → ``GenericDataAddressDTO``

SDK response models (e.g. ``TransferProcessDTO``, ``AssetOutputDTO``) use this type
for their data-address fields so parsed responses carry the correct typed subclass.
"""


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