import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    agreement = client.negotiations.get_agreement("my-negotiation-id")

    log.info("Agreement id: %s", agreement.id)


if __name__ == "__main__":
    main()
