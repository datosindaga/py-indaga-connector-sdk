import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, ContractRequestDTO, OfferDTO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    result = client.negotiations.create(
        ContractRequestDTO(
            context=["https://w3id.org/edc/connector/management/v0.0.1"],
            type="ContractRequest",
            counter_party_address="https://provider.connector/protocol",
            protocol="dataspace-protocol-http",
            policy=OfferDTO(
                id="my-offer-id",
                type="Offer",
                assigner="provider-participant-id",
                target="my-asset-id",
                permission=[
                    {
                        "action": "use",
                    }
                ],
            ),
        )
    )

    log.info("Created negotiation with id: %s", result.id)


if __name__ == "__main__":
    main()
