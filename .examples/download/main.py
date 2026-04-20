import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, DownloadRequest

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    file: bytes = client.download_service.download(
        DownloadRequest(agreement_id="a3fe7fee-b359-477c-ab9d-0f9671601bf4")
    ).file_content

    log.info("File downloaded (%d bytes)", len(file))


if __name__ == "__main__":
    main()