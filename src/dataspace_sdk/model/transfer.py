from enum import Enum
from typing import Any
from pydantic import BaseModel, Field

from dataspace_sdk.model.common import CallbackAddressDTO, DataAddressDTO


class TransferProcessRole(str, Enum):
    CONSUMER = "CONSUMER"
    PROVIDER = "PROVIDER"


class TransferStateEnum(str, Enum):
    REQUESTED = "REQUESTED"
    STARTED = "STARTED"
    SUSPENDED = "SUSPENDED"
    COMPLETED = "COMPLETED"
    TERMINATED = "TERMINATED"
    ERROR = "ERROR"

class TransferProcessDTO(BaseModel):

    context: dict | list | None = Field(None, alias="@context")
    type: str | None = Field(None, alias="@type")
    id: str | None = Field(None, alias="@id")
    role: TransferProcessRole | None = Field(None, alias="type")
    state: TransferStateEnum | None = None
    state_timestamp: int | None = Field(None, alias="stateTimestamp")
    callback_addresses: list[CallbackAddressDTO] = Field(default_factory=list, alias="callbackAddresses")
    correlation_id: str | None = Field(None, alias="correlationId")
    asset_id: str | None = Field(None, alias="assetId")
    contract_id: str | None = Field(None, alias="contractId")
    transfer_type: str | None = Field(None, alias="transferType")
    error_detail: str | None = Field(None, alias="errorDetail")
    data_destination: DataAddressDTO | None = Field(None, alias="dataDestination")

    model_config = {"populate_by_name": True}


class TransferRequestDTO(BaseModel):

    id: str | None = Field(None, alias="@id")
    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    counter_party_address: str | None = Field(None, alias="counterPartyAddress")
    protocol: str | None = None
    contract_id: str | None = Field(None, alias="contractId")
    transfer_type: str | None = Field(None, alias="transferType")
    private_properties: dict[str, Any] = Field(default_factory=dict, alias="privateProperties")
    data_destination: DataAddressDTO | None = Field(None, alias="dataDestination")
    callback_addresses: list[CallbackAddressDTO] = Field(default_factory=list, alias="callbackAddresses")

    model_config = {"populate_by_name": True}


class SuspendTransferDTO(BaseModel):

    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    reason: str | None = None

    model_config = {"populate_by_name": True}


class TransferStateDTO(BaseModel):

    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    state: TransferStateEnum | None = None

    model_config = {"populate_by_name": True}