import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, CatalogRequestDTO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    catalog = client.catalog.get_catalog(
        CatalogRequestDTO(
            counter_party_address="https://provider.connector/protocol",
            counter_party_id="provider-participant-id",
            protocol="dataspace-protocol-http",
            type="CatalogRequest",
            context=["https://w3id.org/edc/connector/management/v0.0.1"],
        )
    )

    log.info("Catalog datasets: %d", len(catalog.dataset))


if __name__ == "__main__":
    main()
