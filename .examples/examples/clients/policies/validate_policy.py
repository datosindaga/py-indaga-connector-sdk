import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    result = client.policies.validate("my-policy-id")

    log.info("Policy valid: %s", result.is_valid)
    if not result.is_valid:
        log.info("Errors: %s", result.errors)


if __name__ == "__main__":
    main()
