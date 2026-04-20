## About The Project

This is the Python SDK of the Flythings Connector Project.

## Build

```bash
pip install flythings-dataspace-sdk
```

## Content

- Auth: This module includes all the authentication logic
- Connector: This module includes all the clients and services that interface with Flythings
  Connector
- Model: This module contains all the required EDC entities

## Requirements

| Tool | Version |
|------|---------|
| Python | 3.9+ |

## Dependencies

### Runtime

| Package | Version | Description |
|---|---|---|
| [`httpx`](https://www.python-httpx.org/) | `>=0.27` | HTTP client with async support |

### Development

| Package | Version | Description |
|---|---|---|
| [`pytest`](https://docs.pytest.org/) | `>=8.0` | Test framework |

## Authentication

Authentication is configured on the `DataspaceClient`, which is the central entry point for the SDK. It supports two authentication strategies: **static token** and **credentials-based**.

> **Note:** Static tokens may expire during long-running operations. If your use case requires uninterrupted access, prefer credentials-based authentication, which handles token renewal automatically.

### Static Token

```python
from flythings_dataspace_sdk import DataspaceClient, TokenAuth

auth = TokenAuth(token="my-token")

client = DataspaceClient(
    base_url="https://sdk.api.url",
    auth=auth,
)
```

### Credentials (Recommended)

```python
from flythings_dataspace_sdk import DataspaceClient, BasicLoginAuth

auth = BasicLoginAuth(
    auth_base_url="https://sdk.auth.url",
    username="my-username",
    password="my-password",
)

client = DataspaceClient(
    base_url="https://sdk.api.url",
    auth=auth,
)
```

When using `BasicLoginAuth`, the client acquires and refreshes tokens automatically, ensuring requests remain authenticated without manual intervention.

An optional `timeout` (in seconds) can be passed to `DataspaceClient`:

```python
from flythings_dataspace_sdk import DataspaceClient, TokenAuth

auth = TokenAuth(token="my-token")

client = DataspaceClient(base_url="my-base-url", auth=auth, timeout=10)
```

### Environment Variables (Recommended for Production)

The SDK can be configured entirely via environment variables using the `from_env()` factory:

```python
from flythings_dataspace_sdk import DataspaceClient

client = DataspaceClient.from_env()
```

The following variables are read automatically:

| Variable | Description |
|---|---|
| `DATASPACE_BASE_URL` | The SDK API base URL |
| `DATASPACE_AUTH_BASE_URL` | The authentication service URL |
| `DATASPACE_USERNAME` | Username for credentials-based auth |
| `DATASPACE_PASSWORD` | Password for credentials-based auth |

---

## Usage

The `DataspaceClient` exposes all clients and services as attributes — no separate instantiation is needed.

### DownloadService

`download_service` downloads the contents of an asset identified by a contract agreement. The response is returned as `bytes`.

**Minimal usage** — only `agreement_id` is required:

```python
from flythings_dataspace_sdk import DataspaceClient, DownloadRequest

client = DataspaceClient.from_env()

file = client.download_service.download(
    DownloadRequest(agreement_id="a3fe7fee-b359-477c-ab9d-0f9671601bf4")
)
```

> **Note:** You can retrieve the `agreement_id` from the web interface. Navigate to **Contracts**, select a contract for your desired asset, click **View Details**, and locate the **Agreement ID** in the Agreement section. ![agreement](.docs/agreement.png)

**Full configuration** — the following shows all available parameters with their defaults:

```python
from flythings_dataspace_sdk import DataspaceClient, DownloadRequest

client = DataspaceClient.from_env()

file = client.download_service.download(
    DownloadRequest(
        agreement_id="a3fe7fee-b359-477c-ab9d-0f9671601bf4",
        transfer_type="HttpData-PUSH",
        data_address_type="HttpProxy",
        protocol="dataspace-protocol-http",
        context=["https://w3id.org/edc/connector/management/v0.0.1"],
    )
)
```

| Parameter | Default | Description |
|---|---|---|
| `transfer_type` | `HttpData-PUSH` | The transfer mechanism used to move the data |
| `data_address_type` | `HttpProxy` | Specifies how the asset's data address is resolved |
| `protocol` | `dataspace-protocol-http` | The dataspace protocol used for the transfer negotiation |
| `context` | EDC management v0.0.1 | JSON-LD `@context` — override when using a custom or domain-specific ontology |

The default configuration assumes an HTTP-based transfer. For non-HTTP assets (e.g., S3, Azure Blob), adjust `transfer_type`, `data_address_type`, and `protocol` accordingly.