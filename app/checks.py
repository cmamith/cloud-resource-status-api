import asyncio
import logging


logger = logging.getLogger(__name__)


async def check_ec2() -> str:
    logger.info("Checking EC2")

    await asyncio.sleep(2)

    logger.info("EC2 check complete")
    return "healthy"


async def check_rds() -> str:
    logger.info("Checking RDS")

    await asyncio.sleep(1)

    logger.info("RDS check complete")
    return "healthy"

# async def check_rds() -> str:
#     logger.info("Checking RDS")

#     await asyncio.sleep(2)

#     raise Exception("RDS API unavailable")


async def check_eks() -> str:
    logger.info("Checking EKS")
    await asyncio.sleep(1)
    return "healthy"

async def run_check(check, timeout: int = 3) -> str:
    try:
        async with asyncio.timeout(timeout):
            return await check()

    except TimeoutError:
        logger.error("Check timed out")
        return "timeout"

    except Exception:
        logger.exception("Check failed")
        return "failed"
    
async def get_platform_status() -> dict[str, str]:

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

def calculate_severity(
    status: dict[str, str]
) -> str:

    unhealthy = sum(
        state != "healthy"
        for state in status.values()
    )

    if unhealthy == 0:
        return "healthy"

    if unhealthy == 1:
        return "degraded"

    return "critical"