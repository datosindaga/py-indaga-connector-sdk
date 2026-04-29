import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    asset_id = "2f0991c8-fe7e-4e92-8731-a874c4bea12d"

    asset = client.assets.get_by_id(asset_id)

    log.info("Found asset with id: %s", asset.properties)


if __name__ == "__main__":
    main()