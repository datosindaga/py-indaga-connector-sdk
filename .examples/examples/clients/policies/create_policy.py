import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, PolicyDefinitionInputDTO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    result = client.policies.create(
        PolicyDefinitionInputDTO(
            context=["https://w3id.org/edc/connector/management/v0.0.1"],
            type="PolicyDefinition",
            private_properties={
                "id": "require-membership",
                "title": "Require Membership",
            },
            policy={
                "@type": "Set",
                "permission": [
                    {
                        "action": "use",
                        "constraint": {
                            "leftOperand": "MembershipCredential",
                            "operator": "eq",
                            "rightOperand": "active",
                        },
                    }
                ],
            },
        )
    )

    log.info("Created policy with id: %s", result.id)


if __name__ == "__main__":
    main()
