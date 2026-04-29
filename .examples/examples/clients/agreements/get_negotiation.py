import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    agreement_id = "1137f1dc-ce3f-4c64-86ce-7629d54aa06a"

    # Retrieve the agreements for my asset
    agreement = client.agreements.get_negotiation_by_agreement_id(agreement_id)

    log.info("Negotiation: %s", agreement)


if __name__ == "__main__":
    main()