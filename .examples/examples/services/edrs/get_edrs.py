import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, GetAgreementEDRsRequest

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    edrs = client.edr_service.get_edrs(
        GetAgreementEDRsRequest(agreement_id="my-agreement-id")
    )

    log.info("EDRs for agreement: %d", len(edrs))


if __name__ == "__main__":
    main()
