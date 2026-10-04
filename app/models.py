from pydantic import BaseModel
from typing import Literal


class InstanceStatus(BaseModel):
    instance_id: str
    region: str
    state: Literal["running", "stopped", "terminated"]


class AIPlatformAnalysis(BaseModel):
    severity: Literal[
        "healthy",
        "degraded",
        "critical"
    ]

    summary: str

    possible_impact: str

    recommended_checks: list[str]


class PlatformStatus(BaseModel):
    ec2: str
    rds: str
    eks: str