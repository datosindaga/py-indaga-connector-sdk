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

## Usage

The `DataspaceClient` exposes all clients and services as attributes — no separate instantiation is needed.

### Clients

Clients map closely to individual API resources. Each client exposes typed methods for a specific domain (e.g., transfers, policies, contract negotiations).

#### Asset Client

`client.assets` exposes the standard CRUD operations for assets.

##### Request

**Minimal usage** — fetch all assets with default pagination:

```python
from flythings_dataspace_sdk import DataspaceClient, QuerySpecDTO

client = DataspaceClient.from_env()

results = client.assets.request(QuerySpecDTO())
```

**Filtered query** — narrow results using `CriterionDTO`:

```python
from flythings_dataspace_sdk import DataspaceClient, QuerySpecDTO, CriterionDTO

client = DataspaceClient.from_env()

results = client.assets.request(
    QuerySpecDTO(
        filter_expression=[
            CriterionDTO(
                operand_left="id",
                operator="=",
                operand_right="my-asset-id",
            )
        ]
    )
)
```

This query is the equivalent of the ``get_by_id`` operation from this same client

- QuerySpecDTO

| Parameter | Type | Default | Description                                      |
|---|---|---|--------------------------------------------------|
| `offset` | `int` | `0` | Number of results to skip                        |
| `limit` | `int` | `50` | Maximum number of results to return              |
| `sort_order` | `"ASC" \| "DESC"` | `"ASC"` | Sort direction                                   |
| `sort_field` | `str` | `None` | Field to sort by (see filterable fields below)   |
| `filter_expression` | `list[CriterionDTO]` | `[]` | List of filter criteria (joined together with AND) |

- CriterionDTO

| Parameter | Description |
|---|---|
| `operand_left` | The field to filter on (see filterable fields below) |
| `operator` | Comparison operator |
| `operand_right` | Value to compare against |

**Supported operators:**

| Operator | Description |
|---|---|
| `=` | Exact match |
| `!=` | Not equal |
| `like` | Wildcard match — use `%` as wildcard (e.g. `my-prefix%`) |
| `in` | Matches any value in a list |
| `contains` | Value is contained in the field's collection |

For the full operator reference see the [EDC Management API docs](https://eclipse-edc.github.io/Connector/openapi/management-api/). Custom versions of EDC might offer more operators like ``ilike``.

- Filterable Asset Fields

Fields can be referenced by their short name or their fully qualified EDC name.

| Short name | Full EDC name | Type | Description |
|---|---|---|---|
| `id` | `https://w3id.org/edc/v0.0.1/ns/id` | `string` | Asset identifier |
| `name` | `https://w3id.org/edc/v0.0.1/ns/name` | `string` | Human-readable name |
| `description` | `https://w3id.org/edc/v0.0.1/ns/description` | `string` | Asset description |
| `contenttype` | `https://w3id.org/edc/v0.0.1/ns/contenttype` | `string` | MIME type of the asset content |
| `createdAt` | `https://w3id.org/edc/v0.0.1/ns/createdAt` | `long` | Creation timestamp (epoch ms) |

> **Note:** This list covers the built-in EDC fields. Assets may carry arbitrary free-form properties under `properties` — these are also filterable using their full key name.

##### Get by ID

Retrieve a single asset by its identifier:

```python
from flythings_dataspace_sdk import DataspaceClient

client = DataspaceClient.from_env()

asset = client.assets.get_by_id("my-asset-id")
```

Returns an `AssetOutputDTO` — identical to `AssetInputDTO` with the addition of a `created_at` timestamp (epoch ms).

##### Create

Register a new asset with its data address:

```python
from flythings_dataspace_sdk import DataspaceClient, AssetInputDTO, DataAddressDTO

client = DataspaceClient.from_env()

id = client.assets.create(
    AssetInputDTO(
        properties={
            "title": "Test TODO",
            "description": "Simple ToDo Json sample for testing with a simple asset",
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
            address_type="HttpData",
            base_url="https://jsonplaceholder.typicode.com/todos",
        ),
    )
)
```

Returns the `id` of the created asset as a `string`.

- AssetInputDTO

| Field | Type | Required | Description |
|---|---|---|---|
| `properties` | `dict` | ✓ | Public asset metadata. See ``Asset Properties`` below |
| `private_properties` | `dict` | | Metadata visible only to the asset owner (e.g. auth details) |
| `data_address` | `DataAddressDTO` | ✓ | Describes where and how the asset data is accessed |

- DataAddressDTO

| Field | Type | Required | Description |
|---|---|---|---|
| `address_type` | `str` | ✓ | Transport type — e.g. `HttpData`, `AmazonS3`, `AzureStorage` |
| `base_url` | `str` | ✓ (for `HttpData`) | Base URL of the data source |
| `additional` | `dict` | | Extra transport-specific fields — e.g. `authKey`, `authCode` for authenticated endpoints |

- Asset Properties

The `properties` dict accepts arbitrary keys. The fields below are the standard EDC-recognised ones plus the ones used by Flythings Connector — any additional keys are stored and indexed as free-form metadata.

| Property | Type | Description                                                   |
|---|---|---------------------------------------------------------------|
| `title` | `str` | Human-readable display name                                   |
| `description` | `str` | Full description of the asset content                         |
| `keywords` | `list[str]` | Tags for discovery and filtering                              |
| `offerType` | `str` | Offering classification (e.g. `Available`, `OnRequest`)       |
| `publicTitle` | `str` | Title shown in the marketplace                                |
| `publicDescription` | `str` | Description shown in the marketplace                                     |
| `theme` | `str` | Thematic category                                             |
| `optOut` | `bool` | When true, the asset will not be publicly listed in the marketplace |

##### Update

Replace an asset's metadata and data address. The target asset is identified by the `id` field on `AssetInputDTO`:

```python
from flythings_dataspace_sdk import DataspaceClient, AssetInputDTO, DataAddressDTO

client = DataspaceClient.from_env()

client.assets.update(
    AssetInputDTO(
        id="my-asset-id",
        properties={
            "title": "Test TODO",
            "description": "Simple ToDo Json sample for testing with a simple asset",
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
            address_type="HttpData",
            base_url="https://jsonplaceholder.typicode.com/todos",
        ),
    )
)
```

Returns `None`. For field descriptions see [Create](#create).

##### Delete

Remove an asset by its identifier:

```python
from flythings_dataspace_sdk import DataspaceClient

client = DataspaceClient.from_env()

client.assets.delete("my-asset-id")
```

Returns `None`.

#### Contract Agreements Client

`client.agreements` provides read access to contract agreements — the binding result of a successfully completed negotiation that authorizes data transfers between two parties. Agreements are read-only; they are produced by the negotiation process and cannot be created or modified directly.

##### Request

Fetch a paginated, filtered list of agreements using [QuerySpecDTO](#Request):

```python
from flythings_dataspace_sdk import DataspaceClient, QuerySpecDTO, CriterionDTO

client = DataspaceClient.from_env()

results = client.agreements.request(
    QuerySpecDTO(
        filter_expression=[
            CriterionDTO(
                operand_left="assetId",
                operator="=",
                operand_right="my-asset-id",
            )
        ]
    )
)
```

Returns `list[ContractAgreementDTO]`.

- Filterable Agreement Fields

| Field | Type | Description |
|---|---|---|
| `id` | `string` | Agreement identifier |
| `assetId` | `string` | Identifier of the asset covered by this agreement |
| `consumerId` | `string` | Participant identifier of the consumer |
| `providerId` | `string` | Participant identifier of the provider |
| `contractSigningDate` | `long` | Signing timestamp (epoch ms) |

##### Get by ID

Retrieve a single agreement by its identifier:

```python
from flythings_dataspace_sdk import DataspaceClient

client = DataspaceClient.from_env()
agreement = client.agreements.get_by_id("my-agreement-id")
```

Returns a `ContractAgreementDTO`.

- ContractAgreementDTO

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Agreement identifier |
| `asset_id` | `str` | Identifier of the asset covered by this agreement |
| `consumer_id` | `str` | Participant identifier of the consuming connector |
| `provider_id` | `str` | Participant identifier of the providing connector |
| `contract_signing_date` | `int` | Signing timestamp (epoch ms) |
| `policy` | `PolicyDTO` | The ODRL policy agreed upon by both parties |

##### Get negotiation

Retrieve the negotiation that produced a given agreement:

```python
from flythings_dataspace_sdk import DataspaceClient

client = DataspaceClient.from_env()
negotiation = client.agreements.get_negotiation_by_agreement_id("my-agreement-id")
```

Returns a `ContractNegotiationDTO`. See [Negotiations Client](#contract-negotiations-client) for field descriptions.

> **Note:** The `agreement_id` returned here is also the identifier passed to `DownloadService` — see [DownloadService](#downloadservice).

#### Transfer Client

`client.transfers` manages the lifecycle of transfer processes — the actual movement of data between connectors, authorized by a contract agreement.

##### Request

Fetch a paginated, filtered list of transfers:

```python
from flythings_dataspace_sdk import DataspaceClient, QuerySpecDTO, CriterionDTO

client = DataspaceClient.from_env()

results = client.transfers.request(
    QuerySpecDTO(
        filter_expression=[
            CriterionDTO(
                operand_left="assetId",
                operator="=",
                operand_right="my-asset-id",
            )
        ]
    )
)
```

Returns `list[TransferProcessDTO]`.

- Filterable Transfer Fields

| Field | Type | Description                                       |
|---|---|---------------------------------------------------|
| `id` | `string` | Transfer process identifier                       |
| `state` | `string` | Current lifecycle state — see `TransferStateEnum` |
| `assetId` | `string` | Identifier of the asset being transferred         |
| `contractId` | `string` | Identifier of the authorizing contract agreement  |
| `transferType` | `string` | Transfer channel and direction — e.g. `HttpData-PUSH` |
| `correlationId` | `string` | Counterparty-side process identifier              |
| `stateTimestamp` | `long` | Timestamp of the last state transition (epoch ms) |

##### Get by ID

Retrieve a single transfer by its identifier:

```python
from flythings_dataspace_sdk import DataspaceClient

client = DataspaceClient.from_env()
transfer = client.transfers.get_by_id("my-transfer-id")
```

Returns a `TransferProcessDTO`.

- TransferProcessDTO

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Transfer process identifier |
| `state` | `TransferStateEnum` | Current lifecycle state |
| `state_timestamp` | `int` | Timestamp of the last state transition (epoch ms) |
| `role` | `TransferProcessRole` | Whether the local connector is `CONSUMER` or `PROVIDER` |
| `asset_id` | `str` | Identifier of the asset being transferred |
| `contract_id` | `str` | Identifier of the authorizing contract agreement |
| `transfer_type` | `str` | Transfer channel and direction |
| `correlation_id` | `str` | Counterparty-side process identifier |
| `data_destination` | `DataAddressDTO` | Destination where data is delivered |
| `error_detail` | `str` | Human-readable error description — populated when state is `ERROR` |
| `callback_addresses` | `list[CallbackAddressDTO]` | Endpoints notified on state changes |

##### Create

Initiate a new transfer process against a contract agreement:

```python
from flythings_dataspace_sdk import DataspaceClient, TransferRequestDTO

client = DataspaceClient.from_env()

result = client.transfers.create(
    TransferRequestDTO(
        counter_party_address="https://provider.connector/protocol",
        protocol="dataspace-protocol-http",
        contract_id="my-agreement-id",
        transfer_type="HttpData-PUSH",
    )
)
```

Returns the `id` of the created transfer as a `string`.

- TransferRequestDTO

| Field | Type | Required | Description |
|---|---|---|---|
| `counter_party_address` | `str` | ✓ | DSP protocol endpoint URL of the counterparty connector |
| `contract_id` | `str` | ✓ | Identifier of the contract agreement authorizing this transfer |
| `transfer_type` | `str` | ✓ | Transfer channel and direction — e.g. `HttpData-PUSH`, `HttpData-PULL` |
| `protocol` | `str` | | Dataspace protocol — typically `dataspace-protocol-http` |
| `data_destination` | `DataAddressDTO` | | Where the transferred data should be delivered |
| `callback_addresses` | `list[CallbackAddressDTO]` | | Endpoints to notify on state changes |
| `private_properties` | `dict` | | Private metadata, not shared externally |

##### Suspend

Temporarily pause an active transfer:

```python
from flythings_dataspace_sdk import DataspaceClient,SuspendTransferDTO

client = DataspaceClient.from_env()
client.transfers.suspend(
    transfer_id="my-transfer-id",
    suspend_transfer=SuspendTransferDTO(reason="Maintenance window"),
)
```

Returns `None`.

##### Resume

Restart a suspended transfer:

```python
from flythings_dataspace_sdk import DataspaceClient

client = DataspaceClient.from_env()
client.transfers.resume("my-transfer-id")
```

Returns `None`.

##### Terminate

Permanently end a transfer before completion:

```python
from flythings_dataspace_sdk import DataspaceClient

client = DataspaceClient.from_env()
client.transfers.terminate("my-transfer-id")
```

Returns `None`.

##### Deprovision

Release any resources provisioned for a completed or terminated transfer:

```python
from flythings_dataspace_sdk import DataspaceClient

client = DataspaceClient.from_env()
client.transfers.deprovision("my-transfer-id")
```

Returns `None`.

#### EDRs (Endpoint Data References) Client

`client.edrs` manages Endpoint Data References — the short-lived access tokens provisioned by the provider once a transfer reaches `STARTED` state. An EDR carries the endpoint and credentials needed to actually retrieve the data.

> **Note:** In most cases you do not need to interact with this client directly. `DownloadService` handles EDR provisioning and data retrieval automatically. Use this client when you need lower-level control over the transfer lifecycle.

##### Request

Fetch a paginated, filtered list of EDRs:

```python
from flythings_dataspace_sdk import DataspaceClient, QuerySpecDTO, CriterionDTO

client = DataspaceClient.from_env()

results = client.edrs.request(
    QuerySpecDTO(
        filter_expression=[
            CriterionDTO(
                operand_left="assetId",
                operator="=",
                operand_right="my-asset-id",
            )
        ]
    )
)
```

Returns `list[EndpointDataReferenceDTO]`.

- Filterable EDR Fields

| Field | Type | Description |
|---|---|---|
| `id` | `string` | EDR identifier |
| `transferProcessId` | `string` | Identifier of the producing transfer process |
| `agreementId` | `string` | Identifier of the authorizing contract agreement |
| `contractNegotiationId` | `string` | Identifier of the originating negotiation |
| `assetId` | `string` | Identifier of the asset made accessible |
| `providerId` | `string` | Identifier of the provider connector |
| `createdAt` | `long` | Creation timestamp (epoch ms) |

##### Get address

Retrieve the resolved data endpoint address for a transfer:

```python
from flythings_dataspace_sdk import DataspaceClient

client = DataspaceClient.from_env()
address = client.edrs.get_address("my-transfer-id")
```

Returns a `DataAddressDTO` containing the endpoint URL and any auth headers provisioned by the provider.

##### Download

Fetch the raw data targeted by an EDR directly:

```python
from flythings_dataspace_sdk import DataspaceClient

client = DataspaceClient.from_env()
data: bytes = client.edrs.download("my-transfer-id")
```

Returns the data as `bytes`. Raises `SdkNotFoundException` if no EDR exists for the given transfer, `SdkUnauthorizedException` if the request is not authenticated.

##### Delete

Deletes a single EDR by its identifier:

```python
from flythings_dataspace_sdk import DataspaceClient

client = DataspaceClient.from_env()
client.edrs.delete("my-transfer-id")
```

Returns `None`.


### Services

Services are higher-level abstractions that either orchestrate multiple clients or encapsulate more complex workflows. Everything that is done with services can be done with clients, services provide ease of use for the more common and complex use cases.

#### DownloadService

`client.download_service` downloads the contents of an asset identified by a contract agreement. The response is returned as `bytes`.

**Minimal usage** — only `agreement_id` is required:

```python
from flythings_dataspace_sdk import DataspaceClient, DownloadRequest

client = DataspaceClient.from_env()

file = client.download_service.download(
    DownloadRequest(agreement_id="a3fe7fee-b359-477c-ab9d-0f9671601bf4")
)
```

> **Note:** You can retrieve the `agreement_id` from the web interface. Navigate to **Contracts**, select a contract for your desired asset, click **View Details**, and locate the **Agreement ID** in the Agreement section.

**Full configuration:**

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