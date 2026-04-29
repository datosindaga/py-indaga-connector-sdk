import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, QuerySpecDTO, CriterionDTO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    edr_id = "b1422a5f-3df6-4880-be29-7efce5a8125e"

    file = client.edrs.download(edr_id)

    log.info("Downloaded file length: %d bytes", len(file))


if __name__ == "__main__":
    main()