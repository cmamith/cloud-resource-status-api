import asyncio
import logging


logger = logging.getLogger(__name__)


async def check_ec2() -> str:
    logger.info("Checking EC2")

    await asyncio.sleep(2)

    logger.info("EC2 check complete")
    return "healthy"


# async def check_rds() -> str:
#     logger.info("Checking RDS")

#     await asyncio.sleep(3)

#     logger.info("RDS check complete")
#     return "healthy"

async def check_rds() -> str:
    logger.info("Checking RDS")

    await asyncio.sleep(2)

    raise Exception("RDS API unavailable")


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