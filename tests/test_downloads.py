from dotenv import load_dotenv

from client import DataspaceClient
from connector.services.download import DownloadRequest

load_dotenv()

def test_download():
    client = DataspaceClient.from_env()

    tes = client.edrs.download("'a4379791-47b8-482b-ae1d-d1797c8e80fe'")

    file = client.download_service.download(
        DownloadRequest(agreement_id="a3fe7fee-b359-477c-ab9d-0f9671601bf4"))
    assert file is not None