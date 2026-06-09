import logging

from dataclasses import dataclass, field

from flythings_dataspace_sdk.connector.clients import ContractAgreementsClient, TransfersClient
from flythings_dataspace_sdk.model import ContractNegotiationDTO, TransferRequestDTO, \
    DataAddressDTO, TransferProcessDTO, SdkBadRequestException

log = logging.getLogger(__name__)

_DEFAULT_PROTOCOL = "dataspace-protocol-http"
_DEFAULT_TRANSFER_TYPE = "HttpData-PULL"
_DEFAULT_DATA_ADDRESS_TYPE = "HttpProxy"
_DEFAULT_CONTEXT = ["https://w3id.org/edc/connector/management/v0.0.1"]

@dataclass
class StartTransferRequest:
    """
    The request sent to the transfer service.

    Attributes:
        agreement_id: the id of the agreement that will be used to create a transfer (Required)
        protocol: the protocol that will be used to retrieve to create a transfer (Optional)
        transfer_type: the type of the transfer that will be used to create a transfer (Optional)
        data_address_type: the type of the data address that will be used to create a transfer (Optional)
        context: the context that will be used to create a transfer (Optional)

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
    request: StartTransferRequest,
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

class TransferService:

    def __init__(self, agreements: ContractAgreementsClient, transfers: TransfersClient):
        self._agreements = agreements
        self._transfers = transfers

    def start_transfer(self, request: StartTransferRequest) -> TransferProcessDTO:
        """
        Start a new transfer from a contract agreement.

        Args:
            request: the transfer request

        Returns:
            A new transfer.
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
        log.info("Transfer process created — id: %s, type: %s",transfer.id, request.transfer_type)

        return self._transfers.get_by_id(transfer.id)


