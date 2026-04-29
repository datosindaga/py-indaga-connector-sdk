import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    transfer_id = "5894962d-3fcd-4ef5-b3a0-b713e6e30cbf"

    transfer = client.transfers.get_by_id(transfer_id)

    log.info("Transfer: %s", transfer)


if __name__ == "__main__":
    main()