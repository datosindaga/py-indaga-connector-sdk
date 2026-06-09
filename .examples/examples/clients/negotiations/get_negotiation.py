import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    negotiation = client.negotiations.get_by_id("my-negotiation-id")

    log.info("Negotiation state: %s", negotiation.state)


if __name__ == "__main__":
    main()
