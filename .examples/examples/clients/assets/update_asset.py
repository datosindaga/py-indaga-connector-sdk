import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, AssetInputDTO, \
    DataAddressDTO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    asset_id = "2f0991c8-fe7e-4e92-8731-a874c4bea12d"

    client.assets.update(
        AssetInputDTO(
            context=["https://w3id.org/edc/connector/management/v0.0.1"],
            type="Asset",
            id=asset_id,
            properties={
                "title": "Updated Test TODO",
                "description": "Simple Updated ToDo Json sample for testing with a simple asset",
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

    log.info("Updated asset with id: %s", asset_id)


if __name__ == "__main__":
    main()