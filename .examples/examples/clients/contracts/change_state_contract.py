import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, ContractState

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    client.contracts.change_state("my-contract-id", ContractState.PUBLISHED)

    log.info("Contract state changed to PUBLISHED")


if __name__ == "__main__":
    main()
