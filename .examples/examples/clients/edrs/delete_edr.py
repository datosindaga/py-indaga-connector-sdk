import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    edr_id = "b1422a5f-3df6-4880-be29-7efce5a8125e"

    client.edrs.delete(edr_id)

    log.info("Deleted reference: %s", edr_id)


if __name__ == "__main__":
    main()