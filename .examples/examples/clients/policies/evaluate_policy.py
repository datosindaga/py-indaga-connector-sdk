import logging
from dotenv import load_dotenv
from flythings_dataspace_sdk import DataspaceClient, PolicyEvaluationPlanRequestDTO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    client = DataspaceClient.from_env()

    plan = client.policies.evaluate(
        policy_id="my-policy-id",
        policy=PolicyEvaluationPlanRequestDTO(
            context=["https://w3id.org/edc/connector/management/v0.0.1"],
            type="PolicyEvaluationPlanRequest",
            policy_scope="catalog",
        ),
    )

    log.info("Permission steps: %d", len(plan.permission_steps))


if __name__ == "__main__":
    main()
