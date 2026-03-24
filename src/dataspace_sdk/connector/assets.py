import httpx

from dataspace_sdk.model.asset import AssetOutputDTO
from dataspace_sdk.model.common import QuerySpecDTO

class AssetsClient:
    _controller = "/v1/assets"

    def __init__(self, client: httpx.Client):
        self._client = client

    def get_assets(self, query: QuerySpecDTO) -> list[AssetOutputDTO]:
        response = self._client.post(
            f"{self._controller}/request",
            json=query,
        )

        return [AssetOutputDTO.model_validate(item) for item in response.json()]