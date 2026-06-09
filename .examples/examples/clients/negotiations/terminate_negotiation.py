import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, TerminationNegotiationDTO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    client.negotiations.terminate("my-negotiation-id")

    client.negotiations.terminate(negotiation_id, TerminationNegotiationDTO(
        context=["https://w3id.org/edc/connector/management/v0.0.1"],
        type="TerminateNegotiation",
        reason="Negotiation terminated by consumer request.",
    ))

    log.info("Terminated negotiation: %s", negotiation_id)


if __name__ == "__main__":
    main()
