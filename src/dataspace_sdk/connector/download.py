import logging

import dataspace_sdk
from dataspace_sdk import DataspaceClient
from dataspace_sdk.connector.agreements import get_negotiation_by_agreement_id
from dataspace_sdk.connector.transfers import create
from dataspace_sdk.model.common import DataAddressDTO
from dataspace_sdk.model.contractnegotiation import ContractNegotiationDTO
from dataspace_sdk.model.transfer import TransferRequestDTO
from dataclasses import dataclass, field

log = logging.getLogger(__name__)

_DEFAULT_PROTOCOL = "dataspace-protocol-http"
_DEFAULT_TRANSFER_TYPE = "HttpData-PULL"
_DEFAULT_DATA_ADDRESS_TYPE = "HttpProxy"
_DEFAULT_CONTEXT = ["https://w3id.org/edc/connector/management/v0.0.1"]

@dataclass
class DownloadResult:
    file_content: bytes
    transfer_id: str

@dataclass
class DownloadRequest:
    agreement_id: str
    protocol: str = _DEFAULT_PROTOCOL
    transfer_type: str = _DEFAULT_TRANSFER_TYPE
    data_address_type: str = _DEFAULT_DATA_ADDRESS_TYPE
    context: list[str] = field(default_factory=lambda: list(_DEFAULT_CONTEXT))

    def __post_init__(self):
        if not self.agreement_id or not self.agreement_id.strip():
            raise ValueError("agreement_id is required")

def _build_transfer_request(
    negotiation: ContractNegotiationDTO,
    request: DownloadRequest,
) -> TransferRequestDTO:
    address = DataAddressDTO(address_type=request.data_address_type)

    return TransferRequestDTO(
        context=request.context,
        protocol=request.protocol,
        transfer_type=request.transfer_type,
        data_destination=address,
        contract_id=negotiation.contract_agreement_id,
        counter_party_address=negotiation.counter_party_address,
    )


def download(client: DataspaceClient, request: DownloadRequest) -> DownloadResult:
    log.info("Starting download for agreement: %s", request.agreement_id)

    log.debug("Fetching contract negotiation...")
    negotiation = get_negotiation_by_agreement_id(client, request.agreement_id)

    log.info("Negotiation resolved — state: %s, counterParty: %s",
             negotiation.state, negotiation.counter_party_address)

    log.debug("Initiating transfer process...")
    transfer = create(client, _build_transfer_request(negotiation, request))
    log.info("Transfer process created — id: %s, type: %s",transfer.id, request.transfer_type)

    log.debug("Downloading data via EDR cache")
    content = dataspace_sdk.connector.edrs.download(client, transfer.id)
    log.info("Download complete — transferId: %s, bytes received: %s", transfer.id, content.__sizeof__())

    return DownloadResult(content, transfer.id)



