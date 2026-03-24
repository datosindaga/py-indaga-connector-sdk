import os

from dotenv import load_dotenv

from dataspace_sdk import download, get_assets
from dataspace_sdk import DataspaceClient
from dataspace_sdk.connector.download import DownloadRequest

load_dotenv()

def test_get_assets():
    client = DataspaceClient.from_env()
    res = get_assets(client)
    print(res)
    assert get_assets(client) is not None


def test_download():
    client = DataspaceClient.from_env()
    file = download(client, DownloadRequest(agreement_id="57876715-4c07-4171-80d6-817f7078c749"))
    assert file is not None