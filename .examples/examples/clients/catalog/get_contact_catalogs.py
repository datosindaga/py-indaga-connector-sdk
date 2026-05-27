import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, ContactRequestDTO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    catalogs = client.catalog.get_contact_catalogs(
        ContactRequestDTO(
            search="drone",
        )
    )

    log.info("Contact catalogs retrieved: %s", catalogs)


if __name__ == "__main__":
    main()
