import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, AssetInputDTO, \
    DataAddressDTO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    asset_id = client.assets.create(
        AssetInputDTO(
            context=["https://w3id.org/edc/connector/management/v0.0.1"],
            type="Asset",
            properties={
                "title": "Test TODO",
                "description": "Simple ToDo Json sample for testing with a simple asset",
                "keywords": ["Test", "TODOs"],
                "offerType": "Available",
                "publicTitle": "Test TODO",
                "publicDescription": "Simple ToDo Json sample for testing with a simple asset",
                "theme": "Testing",
                "optOut": False,
            },
            private_properties={
                "authentication": "REST-API Endpoint",
            },
            data_address=DataAddressDTO(
                type="DataAddress",
                address_type="HttpData",
                base_url="https://jsonplaceholder.typicode.com/todos",
            ),
        )
    )

    log.info("Created asset with id: %s", asset_id.id)


if __name__ == "__main__":
    main()