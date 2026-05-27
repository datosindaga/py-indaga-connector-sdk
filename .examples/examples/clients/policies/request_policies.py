import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, QuerySpecDTO, CriterionDTO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    results = client.policies.request(
        QuerySpecDTO(
            context=["https://w3id.org/edc/connector/management/v0.0.1"],
            type="QuerySpec",
            filter_expression=[
                CriterionDTO(
                    type="Criterion",
                    operand_left="id",
                    operator="=",
                    operand_right="my-policy-id",
                )
            ]
        )
    )

    log.info("Matching policies: %d", len(results))


if __name__ == "__main__":
    main()
