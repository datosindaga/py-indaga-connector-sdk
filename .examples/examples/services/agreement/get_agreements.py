import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, GetAssetAgreementsRequest

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    agreements = client.agreement_service.get_agreements(
        GetAssetAgreementsRequest(asset_id="my-asset-id")
    )

    log.info("Agreements for asset: %d", len(agreements))


if __name__ == "__main__":
    main()
