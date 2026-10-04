from pydantic import BaseModel
from typing import Literal


class InstanceStatus(BaseModel):
    instance_id: str
    region: str
    state: Literal["running", "stopped", "terminated"]