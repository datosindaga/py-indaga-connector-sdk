import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, SuspendTransferDTO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    transfer_id = "8f95e445-093f-46cc-952c-92c70d4c305d"
    reason = "Reason for suspending the transfer"

    client.transfers.suspend(transfer_id, SuspendTransferDTO(
        context=["https://w3id.org/edc/connector/management/v0.0.1"],
        type="SuspendTransfer",
        reason=reason,
    ))

    log.info("Suspended transfer: %s", transfer_id)


if __name__ == "__main__":
    main()