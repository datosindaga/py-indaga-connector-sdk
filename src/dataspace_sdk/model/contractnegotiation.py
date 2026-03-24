from typing import Any
from pydantic import BaseModel, Field

from dataspace_sdk.model.common import CallbackAddressDTO


class ContractNegotiationDTO(BaseModel):

    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    callback_addresses: list[CallbackAddressDTO] = Field(default_factory=list, alias="callbackAddresses")
    contract_agreement_id: str | None = Field(None, alias="contractAgreementId")
    counter_party_address: str | None = Field(None, alias="counterPartyAddress")
    counter_party_id: str | None = Field(None, alias="counterPartyId")
    error_detail: str | None = Field(None, alias="errorDetail")
    protocol: str | None = None
    state: str | None = None
    type_role: str | None = Field(None, alias="type")
    asset_id: str | None = Field(None, alias="assetId")
    private_properties: dict[str, Any] = Field(default_factory=dict, alias="privateProperties")
    created_at: int | None = Field(None, alias="createdAt")

    model_config = {"populate_by_name": True}


class OfferDTO(BaseModel):

    context: dict | list | None = Field(None, alias="@context")
    type: str | None = Field(None, alias="@type")
    id: str | None = Field(None, alias="@id")
    assigner: str | None = None
    target: str | None = None
    permission: list[dict[str, Any]] = Field(default_factory=list)
    prohibition: list[dict[str, Any]] = Field(default_factory=list)
    obligation: list[dict[str, Any]] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


class ContractRequestDTO(BaseModel):

    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    callback_addresses: list[CallbackAddressDTO] = Field(default_factory=list, alias="callbackAddresses")
    counter_party_address: str | None = Field(None, alias="counterPartyAddress")
    policy: OfferDTO | None = None
    protocol: str | None = None
    private_properties: dict[str, Any] = Field(default_factory=dict, alias="privateProperties")

    model_config = {"populate_by_name": True}


class NegotiationStateDTO(BaseModel):

    context: dict | list | None = Field(None, alias="@context")
    state: str | None = None

    model_config = {"populate_by_name": True}


class TerminationNegotiationDTO(BaseModel):

    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    reason: str | None = None

    model_config = {"populate_by_name": True}