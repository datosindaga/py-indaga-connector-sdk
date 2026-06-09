import httpx

from flythings_dataspace_sdk.model import QuerySpecDTO, PolicyDefinitionOutputDTO, \
    PolicyDefinitionInputDTO, IdResponseDTO, PolicyEvaluationPlanRequestDTO, \
    PolicyEvaluationPlanDTO, PolicyValidationResultDTO, PaginatedResultDTO, raise_for_status


class PoliciesClient:
    _controller = "/v1/policydefinitions"

    def __init__(self, client: httpx.Client):
        self._client = client

    def request(self, query: QuerySpecDTO) -> PaginatedResultDTO[PolicyDefinitionOutputDTO]:
        """Retrieves a paginated list of policies matching the given query criteria.

        Args:
            query: The query specification defining filters, pagination, and sorting.

        Returns:
            Paginated result containing matching policies and a flag indicating if more exist.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            f"{self._controller}/request",
            json=query.model_dump(by_alias=True),
        )
        raise_for_status(response)
        return PaginatedResultDTO[PolicyDefinitionOutputDTO].model_validate(response.json())

    def get_by_id(self, policy_id: str) -> PolicyDefinitionOutputDTO:
        """Gets the policy with the matching id.

        Args:
            policy_id: The id of the policy to return.

        Returns:
            The policy with the matching id.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.get(f"{self._controller}/{policy_id}")
        raise_for_status(response)
        return PolicyDefinitionOutputDTO.model_validate(response.json())

    def create(self, policy: PolicyDefinitionInputDTO) -> IdResponseDTO:
        """Creates a new policy.

        Args:
            policy: The policy to be created.

        Returns:
            The id of the created policy.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            self._controller,
            json=policy.model_dump(by_alias=True),
        )
        raise_for_status(response)
        return IdResponseDTO.model_validate(response.json())

    def update(self, policy: PolicyDefinitionInputDTO) -> None:
        """Updates a policy

        Args:
            policy: The policy to be updated. The inner id is used to specify witch existing policy to update.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.put(
            self._controller,
            json=policy.model_dump(by_alias=True),
        )
        raise_for_status(response)

    def delete(self, policy_id: str) -> None:
        """Deletes a policy

        Args:
            policy_id: The policy to be deleted.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.delete(f"{self._controller}/{policy_id}")
        raise_for_status(response)

    def evaluate(self, policy_id: str, policy: PolicyEvaluationPlanRequestDTO) -> PolicyEvaluationPlanDTO:
        """Creates a new policy evaluation plan.

        Args:
            policy_id: The target policy id
            policy: The policy evaluation plan to be created.

        Returns:
            The plan.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            f"{self._controller}/{policy_id}/evaluationplan",
            json=policy.model_dump(by_alias=True),
        )
        raise_for_status(response)
        return PolicyEvaluationPlanDTO.model_validate(response.json())

    def validate(self, policy_id: str) -> PolicyValidationResultDTO:
        """Validates a policy.

        Args:
            policy_id: The policy to be validated.

        Returns:
            The validation result.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
        """
        response = self._client.post(
            f"{self._controller}/{policy_id}/validate",
        )
        raise_for_status(response)
        return PolicyValidationResultDTO.model_validate(response.json())