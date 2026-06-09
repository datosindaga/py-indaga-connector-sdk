import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, QuerySpecDTO, CriterionDTO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    # Find the assets of theme "Testing", that are not "Unavailable" with the keyword "Test"
    assets = client.assets.request(
        QuerySpecDTO(
            context=["https://w3id.org/edc/connector/management/v0.0.1"],
            type="QuerySpec",
            filter_expression=[
                CriterionDTO(
                    type="Criterion",
                    operand_left="https://w3id.org/edc/v0.0.1/ns/theme",
                    operator="=",
                    operand_right="Testing",
                ),
                CriterionDTO(
                    type="Criterion",
                    operand_left="https://w3id.org/edc/v0.0.1/ns/offerType",
                    operator="!=",
                    operand_right="Unavailable",
                ),
                CriterionDTO(
                    type="Criterion",
                    operand_left="https://w3id.org/edc/v0.0.1/ns/keywords",
                    operator="contains",
                    operand_right=["Test"],
                )
            ]
        )
    )

    log.info("Matching assets: %d", len(assets.items))


if __name__ == "__main__":
    main()