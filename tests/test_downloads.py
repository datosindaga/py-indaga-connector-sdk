import logging

from dotenv import load_dotenv

from flythings_dataspace_sdk import DataspaceClient, DownloadRequest

load_dotenv()
logging.basicConfig(level=logging.INFO)

def test_download():
    client = DataspaceClient.from_env()

    file = client.download_service.download(
        DownloadRequest(agreement_id="a3fe7fee-b359-477c-ab9d-0f9671601bf4"))
    assert file is not None