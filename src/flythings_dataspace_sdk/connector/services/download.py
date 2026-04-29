import logging
import time

from dataclasses import dataclass, field

from flythings_dataspace_sdk.connector.clients import ContractAgreementsClient, TransfersClient, EDRSClient
from flythings_dataspace_sdk.model import ContractNegotiationDTO, TransferRequestDTO, \
    DataAddressDTO, TransferStateEnum, SdkServerException, SdkBadRequestException

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

        if negotiation.state == "TERMINATED":
            raise SdkBadRequestException(
                f"Contract negotiation is TERMINATED for agreement: {request.agreement_id}"
            )

        log.info("Negotiation resolved — state: %s, counterParty: %s",
                 negotiation.state, negotiation.counter_party_address)

        log.debug("Initiating transfer process...")
        transfer = self._transfers.create(
            _build_transfer_request(negotiation, request))
        log.info("Transfer process created — id: %s, type: %s", transfer.id,
                 request.transfer_type)

        log.debug("Waiting for transfer to reach STARTED state...")
        self._wait_for_transfer_started(transfer.id)

        log.debug("Downloading data via EDR cache")
        content = self._edrs.download(transfer.id)
        log.info("Download complete — transferId: %s, bytes received: %s", transfer.id, content.__sizeof__())

        return DownloadResult(content, transfer.id)

    def _wait_for_transfer_started(self, transfer_id: str, *,
        max_attempts: int = 10, base_delay: float = 1.0) -> None:
        """Polls until the transfer process reaches STARTED state."""
        time.sleep(5)
        for attempt in range(1, max_attempts + 1):
            transfer = self._transfers.get_by_id(transfer_id)
            if transfer.state == TransferStateEnum.STARTED:
                log.debug("Transfer STARTED after %d attempt(s)", attempt)
                return
            if transfer.state in (TransferStateEnum.TERMINATED,
                                  TransferStateEnum.ERROR):
                raise SdkServerException(
                    f"Transfer {transfer_id!r} reached terminal state: {transfer.state}")
            if attempt == max_attempts:
                raise TimeoutError(
                    f"Transfer {transfer_id!r} still in state {transfer.state} after {max_attempts} attempts")
            delay = base_delay * (2 ** (attempt - 1))
            log.debug(
                "Transfer state is %s (attempt %d/%d), retrying in %.1fs...",
                transfer.state, attempt, max_attempts, delay)
            time.sleep(delay)


