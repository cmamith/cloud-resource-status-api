import logging

from app.models import InstanceStatus


logger = logging.getLogger(__name__)


instances = {
    "i-001": {
        "instance_id": "i-001",
        "region": "ap-northeast-1",
        "state": "running"
    },
    "i-002": {
        "instance_id": "i-002",
        "region": "ap-northeast-1",
        "state": "running"
    }
}


def get_instance_status(instance_id: str) -> InstanceStatus | None:
    logger.info("Checking instance %s", instance_id)

    instance = instances.get(instance_id)

    if instance is None:
        logger.warning("Instance %s not found", instance_id)
        return None

    logger.info(
        "Instance %s found with state %s",
        instance_id,
        instance["state"]
    )

    return InstanceStatus(**instance)

def get_all_instances() -> list[InstanceStatus]:
    return [
        InstanceStatus(**instance)
        for instance in instances.values()
    ]

