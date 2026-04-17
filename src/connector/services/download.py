import logging

from connector.clients.contract_agreements import ContractAgreementsClient
from connector.clients.edrs import EDRSClient
from connector.clients.transfers import TransfersClient
from model.common import DataAddressDTO
from model.contractnegotiation import ContractNegotiationDTO
from model.transfer import TransferRequestDTO
from dataclasses import dataclass, field

log = logging.getLogger(__name__)

_DEFAULT_PROTOCOL = "dataspace-protocol-http"
_DEFAULT_TRANSFER_TYPE = "HttpData-PULL"
_DEFAULT_DATA_ADDRESS_TYPE = "HttpProxy"
_DEFAULT_CONTEXT = ["https://w3id.org/edc/connector/management/v0.0.1"]

@dataclass
class DownloadResult:
    """
    The result of the download.

    Attributes:
        file_content: the bytes of the downloaded file.
        transfer_id: the id of the transfer generated during the download.
    """
    file_content: bytes
    transfer_id: str

@dataclass
class DownloadRequest:
    """
    The request sent to the download service.

    Attributes:
        agreement_id: the id of the agreement that will be used to start the download (Required)
        protocol: the protocol that will be used for the transfer (Optional)
        transfer_type: the type of the transfer that will be used for the transfer (Optional)
        data_address_type: the type of the data address that will be used for the transfer (Optional)
        context: the context that will be used for the transfer (Optional)

    """
    agreement_id: str
    protocol: str = _DEFAULT_PROTOCOL
    transfer_type: str = _DEFAULT_TRANSFER_TYPE
    data_address_type: str = _DEFAULT_DATA_ADDRESS_TYPE
    context: list[str] = field(default_factory=lambda: list(_DEFAULT_CONTEXT))

    def __post_init__(self):
        if not self.agreement_id or not self.agreement_id.strip():
            raise ValueError("agreement_id is required")


def _build_transfer_request(negotiation: ContractNegotiationDTO,
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

class DownloadService:

    def __init__(self, agreements: ContractAgreementsClient, transfers: TransfersClient, edrs: EDRSClient):
        self._agreements = agreements
        self._transfers = transfers
        self._edrs = edrs

    def download(self, request: DownloadRequest) -> DownloadResult:
        """
        Executes the full download workflow for the given contract agreement.

        Args:
            request: the request sent to the download service.

        Returns:
            The result of the download.
        """
        log.info("Starting download for agreement: %s", request.agreement_id)

        log.debug("Fetching contract negotiation...")
        negotiation = self._agreements.get_negotiation_by_agreement_id(request.agreement_id)

        log.info("Negotiation resolved — state: %s, counterParty: %s",
                 negotiation.state, negotiation.counter_party_address)

        log.debug("Initiating transfer process...")
        transfer = self._transfers.create(
            _build_transfer_request(negotiation, request))
        log.info("Transfer process created — id: %s, type: %s",transfer.id, request.transfer_type)

        log.debug("Downloading data via EDR cache")
        content = self._edrs.download(transfer.id)
        log.info("Download complete — transferId: %s, bytes received: %s", transfer.id, content.__sizeof__())

        return DownloadResult(content, transfer.id)


