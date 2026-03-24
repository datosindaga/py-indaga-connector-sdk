from typing import Any

from pydantic import BaseModel, Field

class PolicyDTO(BaseModel):

    context: dict | list | None = Field(None, alias="@context")
    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    action: list[dict[str, Any]] = Field(default_factory=list)
    permission: list[dict[str, Any]] = Field(default_factory=list)
    prohibition: list[dict[str, Any]] = Field(default_factory=list)
    obligation: list[dict[str, Any]] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


class ContractAgreementDTO(BaseModel):

    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    asset_id: str | None = Field(None, alias="assetId")
    consumer_id: str | None = Field(None, alias="consumerId")
    provider_id: str | None = Field(None, alias="providerId")
    contract_signing_date: int | None = Field(None, alias="contractSigningDate")
    policy: PolicyDTO | None = None

    model_config = {"populate_by_name": True}