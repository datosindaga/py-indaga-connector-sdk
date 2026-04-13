import logging
from dataclasses import field, dataclass

from dataspace_sdk.connector.clients.edrs import EDRSClient
from dataspace_sdk.model.common import QuerySpecDTO, CriterionDTO
from dataspace_sdk.model.edr import EndpointDataReferenceDTO

log = logging.getLogger(__name__)

_DEFAULT_CONTEXT = ["https://w3id.org/edc/connector/management/v0.0.1"]

@dataclass
class EdrRequest:
    """
    The request sent to the edr service.

    Attributes:
        agreement_id: the id of the agreement that will be used to retrieve the edrs (Required)
        context: the context that will be used (Optional)

    """
    agreement_id: str
    context: list[str] = field(default_factory=lambda: list(_DEFAULT_CONTEXT))

    def __post_init__(self):
        if not self.agreement_id or not self.agreement_id.strip():
            raise ValueError("agreement_id is required")

class EdrService:

    def __init__(self, edrs: EDRSClient):
        self._edrs = edrs

    def get_edrs(self, request: EdrRequest) -> list[EndpointDataReferenceDTO]:
        """
        Get the edrs related to an agreement.

        Parameters:
             request: the edrs request

        Returns:
            The list of edrs related to an agreement.
        """
        log.info("Fetching EDRs for agreement: %s", request.agreement_id)

        query = QuerySpecDTO(
            type="QuerySpec",
            context=request.context,
            filter_expression=[
                CriterionDTO(
                    type="Criterion",
                    operand_left="agreementId",
                    operator="=",
                    operand_right=request.agreement_id,
                )
            ],
        )

        return self._edrs.request(query=query)
