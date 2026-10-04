import asyncio
import pytest

from app.checks import run_check


@pytest.mark.asyncio
async def test_run_check_success():

    async def successful_check():
        await asyncio.sleep(0.1)
        return "healthy"

    result = await run_check(
        successful_check,
        timeout=1
    )

    assert result == "healthy"


@pytest.mark.asyncio
async def test_run_check_failure():

    async def failing_check():
        raise Exception("API unavailable")

    result = await run_check(
        failing_check,
        timeout=1
    )

    assert result == "failed"


@pytest.mark.asyncio
async def test_run_check_timeout():

    async def slow_check():
        await asyncio.sleep(2)
        return "healthy"

    result = await run_check(
        slow_check,
        timeout=0.1
    )

    assert result == "timeout"