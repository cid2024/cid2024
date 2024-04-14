import asyncio
from llm.ai_handler import AiHandler
from llm.utils import run_prompt
from settings.config_loader import get_settings

if __name__ == "__main__":
    handler = AiHandler()

    prompt = get_settings()["ask_capital_city_prompt"]

    response = asyncio.run(
        run_prompt(
            handler,
            prompt,
            user_vars={
                "country": "  Chocopie  ",
            },
            system_vars=dict(),
        )
    )


    print(f"{response = }")
