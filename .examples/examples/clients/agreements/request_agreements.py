import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, QuerySpecDTO, CriterionDTO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    asset_id = "0f34e1a8-4dc0-4916-bc18-393bf71888b3"

    # Retrieve the agreements for my asset
    edrs = client.agreements.request(
        QuerySpecDTO(
            context=["https://w3id.org/edc/connector/management/v0.0.1"],
            type="QuerySpec",
            filter_expression=[
                CriterionDTO(
                    type="Criterion",
                    operand_left="assetId",
                    operator="=",
                    operand_right=asset_id,
                )
            ]
        )
    )

    log.info("Matching edrs for the specified asset: %d", len(edrs))


if __name__ == "__main__":
    main()