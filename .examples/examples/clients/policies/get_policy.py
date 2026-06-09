import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    policy = client.policies.get_by_id("my-policy-id")

    log.info("Found policy with id: %s", policy.id)


if __name__ == "__main__":
    main()
