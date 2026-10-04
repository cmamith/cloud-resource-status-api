import json
import os

from openai import AsyncOpenAI

from app.models import AIPlatformAnalysis


client = AsyncOpenAI()

MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-6-astra"
)


async def analyze_platform_status(
    status: dict[str, str],
    severity: str
) -> AIPlatformAnalysis:

    response = await client.responses.parse(
    model=MODEL,
    input=[
        {
            "role": "system",
            "content": (
                "You are an assistant for a cloud platform engineering team. "
                "Analyze only the supplied service health data. "
                "Do not invent metrics, incidents, root causes, or infrastructure details. "
                "The platform severity is calculated by the application. "
                "Do not change or reinterpret the supplied severity. "
                "Give concise operational guidance."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Platform severity: {severity}\n"
                f"Health status:\n"
                + json.dumps(status, indent=2)
            ),
        },
    ],
    text_format=AIPlatformAnalysis,
)

    if response.output_parsed is None:
        raise RuntimeError(
            "AI analysis did not return structured output"
        )

    return response.output_parsed