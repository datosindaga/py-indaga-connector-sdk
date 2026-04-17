from enum import Enum
from typing import Any
from pydantic import BaseModel, Field

from model.common import CallbackAddressDTO, DataAddressDTO


class TransferProcessRole(str, Enum):
    """Represents the role of a participant in a transfer process.

    Attributes:
        CONSUMER: The party requesting and receiving the transferred data.
        PROVIDER: The party supplying and sending the transferred data.
    """
    CONSUMER = "CONSUMER"
    PROVIDER = "PROVIDER"


class TransferStateEnum(str, Enum):
    """Enumerates the possible lifecycle states of a transfer process.

    Attributes:
        INITIAL: The transfer has been requested but not yet started.
        STARTED: The transfer is actively in progress.
        SUSPENDED: The transfer has been temporarily paused.
        COMPLETED: The transfer finished successfully.
        TERMINATED: The transfer was ended before completion, typically by one of the parties.
        ERROR: The transfer encountered an unrecoverable error.
    """
    INITIAL = "INITIAL"
    REQUESTED = "REQUESTED"
    STARTED = "STARTED"
    SUSPENDED = "SUSPENDED"
    COMPLETED = "COMPLETED"
    TERMINATED = "TERMINATED"
    ERROR = "ERROR"


class TransferProcessDTO(BaseModel):
    """Represents a transfer process as returned by the dataspace connector.

    This DTO maps to the response body of transfer process query and fetch endpoints.
    Fields are deserialized from JSON-LD — use ``model_validate`` with aliased keys
    when parsing connector responses.

    Attributes:
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        type: JSON-LD type of the transfer process, typically ``TransferProcess``.
        id: JSON-LD identifier of the transfer process. Example: ``urn:uuid:a1b2c3d4-...``
        role: Whether the local connector is acting as ``CONSUMER`` or ``PROVIDER``.
        state: Current lifecycle state of the transfer process.
        state_timestamp: Unix epoch timestamp (ms) of the last state transition.
        callback_addresses: List of callback endpoints notified on state changes.
        correlation_id: Identifier used to correlate this process with a counterparty process.
        asset_id: Identifier of the asset being transferred.
        contract_id: Identifier of the contract agreement governing this transfer.
        transfer_type: Describes the transfer channel and direction, e.g. ``HttpData-PULL``.
        error_detail: Human-readable error description, populated when state is ``ERROR``.
        data_destination: Describes where the data should be delivered to.
    """
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
    """Represents the input payload for initiating a transfer process.

    This DTO is sent as the request body to the transfer process initiation endpoint.
    Fields are serialized using JSON-LD conventions — use ``model_dump(by_alias=True)``
    when building the request payload.

    Attributes:
        id: Optional JSON-LD identifier to assign to the transfer process.
        type: JSON-LD type, typically ``TransferRequest``.
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        counter_party_address: DSP protocol endpoint URL of the counterparty connector.
        protocol: Dataspace protocol to use, e.g. ``dataspace-protocol-http``.
        contract_id: Identifier of the contract agreement authorising this transfer.
        transfer_type: Describes the transfer channel and direction, e.g. ``HttpData-PULL``.
        private_properties: Private metadata attached to the transfer, not shared externally.
        data_destination: Describes where the transferred data should be delivered.
        callback_addresses: List of callback endpoints to be notified on state changes.
    """
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
    """Represents the input payload for suspending an active transfer process.

    This DTO is sent as the request body to the transfer process suspend endpoint.
    Fields are serialized using JSON-LD conventions — use ``model_dump(by_alias=True)``
    when building the request payload.

    Attributes:
        type: JSON-LD type, typically ``SuspendTransfer``.
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        reason: Human-readable explanation of why the transfer is being suspended.
    """
    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    reason: str | None = None

    model_config = {"populate_by_name": True}


class TransferStateDTO(BaseModel):
    """Represents the current state of a transfer process as a lightweight response body.

    This DTO is typically returned by state-query endpoints that report only the
    current lifecycle state rather than the full transfer process representation.

    Attributes:
        type: JSON-LD type, typically ``TransferState``.
        context: JSON-LD context, either as a vocabulary object or a list of context URLs.
        state: Current lifecycle state of the transfer process.
    """
    type: str | None = Field(None, alias="@type")
    context: dict | list | None = Field(None, alias="@context")
    state: TransferStateEnum | None = None

    model_config = {"populate_by_name": True}