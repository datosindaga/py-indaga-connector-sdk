from enum import Enum

from pydantic import BaseModel, Field
from typing import Any


class IdResponseDTO(BaseModel):
    id: str = Field(alias="@id")
    type: str = Field(alias="@type")

    model_config = {"populate_by_name": True}

class CriterionDTO(BaseModel):
    type: str | None = Field(None, alias="@type")
    operand_left: str = Field(alias="operandLeft")
    operand_right: Any = Field(alias="operandRight")
    operator: str

    model_config = {"populate_by_name": True}

class CallbackAddressDTO(BaseModel):

    type: str | None = Field(None, alias="@type")
    auth_code_id: str | None = Field(None, alias="authCodeId")
    auth_key: str | None = Field(None, alias="authKey")
    events: list[str] = Field(default_factory=list)
    transactional: bool | None = None
    uri: str | None = None

    model_config = {"populate_by_name": True}


class DataAddressDTO(BaseModel):

    type: str | None = Field(None, alias="@type")
    address_type: str | None = Field(None, alias="type")
    base_url: str | None = Field(None, alias="baseUrl")
    proxy_path: bool | None = Field(None, alias="proxyPath")
    proxy_query_params: bool | None = Field(None, alias="proxyQueryParams")
    endpoint: str | None = None
    authorization: str | None = None

    model_config = {"populate_by_name": True, "extra": "allow"}
    # Extra allows for additional non defined fields

class SortOrder(str, Enum):

    ASC = "ASC"
    DESC = "DESC"


class QuerySpecDTO(BaseModel):

    context: dict | list | None = Field(None, alias="@context")
    type: str | None = Field(None, alias="@type")
    offset: int | None = None
    limit: int | None = None
    sort_field: str | None = Field(None, alias="sortField")
    sort_order: SortOrder | None = Field(None, alias="sortOrder")
    filter_expression: list[CriterionDTO] = Field(default_factory=list, alias="filterExpression")

    model_config = {"populate_by_name": True}