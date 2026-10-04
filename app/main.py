from fastapi import FastAPI, HTTPException
import asyncio
from app.services import (
    get_instance_status,
    get_all_instances
)
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.checks import check_ec2, check_rds, check_eks, run_check

from app.models import InstanceStatus
from app.services import get_instance_status

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

app = FastAPI(
    title="Cloud Resource Status API",
    version="0.1.0"
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

templates = Jinja2Templates(
    directory="app/templates"
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get(
    "/instances/{instance_id}",
    response_model=InstanceStatus
)
def get_instance(instance_id: str) -> InstanceStatus:
    instance = get_instance_status(instance_id)

    if instance is None:
        raise HTTPException(
            status_code=404,
            detail="Instance not found"
        )

    return instance


@app.get("/platform-status")
async def platform_status() -> dict[str, str]:

    ec2, rds, eks = await asyncio.gather(
        run_check(check_ec2),
        run_check(check_rds),
        run_check(check_eks)
    )

    return {
        "ec2": ec2,
        "rds": rds,
        "eks": eks
    }

@app.get(
    "/instances",
    response_model=list[InstanceStatus]
)
def list_instances() -> list[InstanceStatus]:
    return get_all_instances()


@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={}
    )