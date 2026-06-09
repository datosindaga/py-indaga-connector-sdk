import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, QuerySpecDTO, CriterionDTO, \
    TransferRequestDTO, DataAddressDTO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    contract = "a3fe7fee-b359-477c-ab9d-0f9671601bf4"
    url = "https://devdsconnector.flythings.io/cp/api/dsp"

    identifier = client.transfers.create(
        TransferRequestDTO(
            context=["https://w3id.org/edc/connector/management/v0.0.1"],
            type="TransferRequest",
            protocol="dataspace-protocol-http",
            transfer_type="HttpData-PULL",
            data_destination=DataAddressDTO(address_type="HttpProxy"),
            contract_id=contract,
            counter_party_address=url,
        )
    )

    log.info("Id: %s", identifier.id)


if __name__ == "__main__":
    main()