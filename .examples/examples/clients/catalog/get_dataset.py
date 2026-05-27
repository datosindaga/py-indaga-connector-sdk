import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, DatasetRequestDTO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    dataset = client.catalog.get_dataset(
        DatasetRequestDTO(
            id="my-asset-id",
            counter_party_address="https://provider.connector/protocol",
            counter_party_id="provider-participant-id",
            protocol="dataspace-protocol-http",
            type="DatasetRequest",
            context=["https://w3id.org/edc/connector/management/v0.0.1"],
        )
    )

    log.info("Dataset id: %s", dataset.id)


if __name__ == "__main__":
    main()
