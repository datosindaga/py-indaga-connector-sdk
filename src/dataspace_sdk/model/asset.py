from pydantic import BaseModel, Field

from dataspace_sdk.model.common import DataAddressDTO


class AssetInputDTO(BaseModel):
    """Represents the input payload for creating or updating an asset in the dataspace connector.

    This DTO is typically sent as the request body to POST or PUT asset endpoints.
    Fields are serialized using JSON-LD conventions — use `model_dump(by_alias=True)`
    when building the request payload.

    Attributes:
        id: JSON-LD identifier of the asset. Example: ``urn:uuid:3b3c1a7e-482d-4c8a-8a22-1e7462a4c456``
        type: JSON-LD type of the asset, typically ``Asset``.
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        data_address: Describes how and where the asset's data can be accessed.
        properties: Public metadata properties of the asset (e.g. name, contentType).
        private_properties: Private metadata not exposed to other participants.
    """
    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    data_address: DataAddressDTO | None = Field(None, alias="dataAddress")
    properties: dict[str, object] = Field(default_factory=dict)
    private_properties: dict[str, object] = Field(default_factory=dict, alias="privateProperties")

    model_config = {"populate_by_name": True}


class AssetOutputDTO(BaseModel):
    """Represents the output payload of an asset in the dataspace connector.

    This DTO is typically the response body multiple requests.

    Attributes:
        id: JSON-LD identifier of the asset. Example: ``urn:uuid:3b3c1a7e-482d-4c8a-8a22-1e7462a4c456``
        type: JSON-LD type of the asset, typically ``Asset``.
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        data_address: Describes how and where the asset's data can be accessed.
        properties: Public metadata properties of the asset (e.g. name, contentType).
        private_properties: Private metadata not exposed to other participants.
        created_at: the date of creation as an instant
    """
    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    context: dict[str, object] = Field(default_factory=dict, alias="@context")
    created_at: int | None = Field(None, alias="createdAt")
    properties: dict[str, object] = Field(default_factory=dict)
    private_properties: dict[str, object] = Field(default_factory=dict, alias="privateProperties")
    data_address: DataAddressDTO | None = Field(None, alias="dataAddress")

    model_config = {"populate_by_name": True}