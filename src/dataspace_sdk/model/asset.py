from pydantic import BaseModel, Field

from dataspace_sdk.model.common import DataAddressDTO


class AssetInputDTO(BaseModel):

    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    data_address: DataAddressDTO | None = Field(None, alias="dataAddress")
    properties: dict[str, object] = Field(default_factory=dict)
    private_properties: dict[str, object] = Field(default_factory=dict, alias="privateProperties")

    model_config = {"populate_by_name": True}


class AssetOutputDTO(BaseModel):

    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    context: dict[str, object] = Field(default_factory=dict, alias="@context")
    created_at: int | None = Field(None, alias="createdAt")
    properties: dict[str, object] = Field(default_factory=dict)
    private_properties: dict[str, object] = Field(default_factory=dict, alias="privateProperties")
    data_address: DataAddressDTO | None = Field(None, alias="dataAddress")

    model_config = {"populate_by_name": True}