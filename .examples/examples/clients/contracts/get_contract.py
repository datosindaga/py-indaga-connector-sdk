import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    contract = client.contracts.get_by_id("my-contract-id")

    log.info("Found contract with id: %s", contract.id)


if __name__ == "__main__":
    main()
