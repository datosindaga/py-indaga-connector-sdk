## [1.1.0](https://github.com/datosindaga/py-indaga-connector-sdk/releases/tag/v1.1.0) (09/06/2026)

#### New

- Added `AssetClient` (create, get, update, delete, request)
- Added `CatalogClient` (get catalog, get dataset, get contact catalogs)
- Added `ContractDefinitionClient` (create, get, update, delete, request, change state)
- Added `ContractNegotiationClient` (create, get, get state, get agreement, terminate, hide, delete, request)
- Added `PolicyClient` (create, get, update, delete, request, evaluate, validate)
- Added full examples module covering all clients and services
- Added `PaginatedResultDTO` for paginated query results

#### Fixed

- Several clients not raising `SdkException` on error responses
- `GetAssetAgreementsRequest` returning incorrect response type
- `SuspendTransfer` missing `@context` and `@type` fields
- `TerminateTransfer` missing body — added `TerminateTransferDTO`, updated client and example
- `TerminateNegotiation` missing body — wired `TerminationNegotiationDTO` into client and example
- Catalog models incompatible with Python 3.9 due to missing `from __future__ import annotations`

## [1.0.2](https://github.com/datosindaga/py-indaga-connector-sdk/releases/tag/v1.0.2) (24/04/2026)

#### New

- Added download example in .examples

#### Fixed

- Added missing dependency

## [1.0.1](https://github.com/datosindaga/py-indaga-connector-sdk/releases/tag/v1.0.1) (24/04/2026)

#### Breaking changes

- Moved all packages to `flythings_dataspace_sdk`. Fixed issue with private classes

## [1.0.0](https://github.com/datosindaga/py-indaga-connector-sdk/releases/tag/v1.0.0) (17/04/2026)

#### New

- Added Authentication
- Added Client for transfers
- Added Client for contract agreements
- Added Client for EDR Caches
- Added Download Service
