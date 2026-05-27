import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, StartTransferRequest

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    transfer = client.transfer_service.start_transfer(
        StartTransferRequest(agreement_id="my-agreement-id")
    )

    log.info("Transfer started with id: %s, state: %s", transfer.id, transfer.state)


if __name__ == "__main__":
    main()
