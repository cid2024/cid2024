from typing import Any, Literal

from jinja2 import Template

from llm.ai_handler import AiHandler
from settings.config_loader import get_settings


async def run_prompt(
    handler: AiHandler,
    prompt: dict[str, Any],
    user_vars: dict[str, Any] | None = None,
    system_vars: dict[str, Any] | None = None,
) -> str:
    if not user_vars:
        user_vars = dict()

    if not system_vars:
        system_vars = dict()

    system_msg = Template(prompt.system).render(**system_vars)
    user_msg = Template(prompt.user).render(**user_vars)

    temperature = prompt.get("temperature", None)
    frequency_penalty = prompt.get("frequency_penalty", None)

    response, _ = await handler.chat_completion(
        model_name=prompt.get("model"),
        system=system_msg,
        user=user_msg,
        temperature=temperature,
        frequency_penalty=frequency_penalty,
    )

    return response
