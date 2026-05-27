import logging
from dataclasses import field, dataclass

from flythings_dataspace_sdk.connector.clients import ContractAgreementsClient
from flythings_dataspace_sdk.model import ContractAgreementDTO, QuerySpecDTO, \
    CriterionDTO

log = logging.getLogger(__name__)

_DEFAULT_CONTEXT = ["https://w3id.org/edc/connector/management/v0.0.1"]

@dataclass
class GetAssetAgreementsRequest:
    """
    The request sent to the agreements service.

    Attributes:
        asset_id: the id of the asset that will be used to retrieve the agreements (Required)
        context: the context that will be used (Optional)

    """
    asset_id: str
    context: list[str] = field(default_factory=lambda: list(_DEFAULT_CONTEXT))

    def __post_init__(self):
        if not self.asset_id or not self.asset_id.strip():
            raise ValueError("asset_id is required")

class AgreementService:

    def __init__(self, agreements: ContractAgreementsClient):
        self._agreements = agreements

    def get_agreements(self, request: GetAssetAgreementsRequest) -> list[ContractAgreementDTO]:
        """
        Get the agreements related to an asset.

        Parameters:
             request: the agreements request

        Returns:
            The list of agreements related to an asset.
        """
        log.info("Fetching agreements for asset: %s", request.asset_id)

        query = QuerySpecDTO(
            type="QuerySpec",
            context=request.context,
            filter_expression=[
                CriterionDTO(
                    type="Criterion",
                    operand_left="assetId",
                    operator="=",
                    operand_right=request.asset_id,
                )
            ],
        )

        return self._agreements.request(query=query)
