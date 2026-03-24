from dataspace_sdk.auth.client import DataspaceClient
from dataspace_sdk.model.common import QuerySpecDTO


def get_assets(client: DataspaceClient, query: QuerySpecDTO) -> dict:
    response = client.post(
        "/v1/assets/request",
        json=query,
    )

    return response.json()