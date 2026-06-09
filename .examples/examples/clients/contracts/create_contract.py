import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, ContractDefinitionInputDTO, CriterionDTO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    result = client.contracts.create(
        ContractDefinitionInputDTO(
            context=["https://w3id.org/edc/connector/management/v0.0.1"],
            type="ContractDefinition",
            access_policy_id="my-access-policy-id",
            contract_policy_id="my-contract-policy-id",
            assets_selector=[
                CriterionDTO(
                    type="Criterion",
                    operand_left="id",
                    operator="=",
                    operand_right="my-asset-id",
                )
            ],
        )
    )

    log.info("Created contract with id: %s", result.id)


if __name__ == "__main__":
    main()
