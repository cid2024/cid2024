import asyncio

from llm.ai_handler import AiHandler


if __name__ == "__main__":
    handler = AiHandler()

    response, _ = asyncio.run(
        handler.chat_completion(
            system="You are a kind assistant.",
            user="What is the capital city of Chocopie?",
        )
    )

    print(f"{response = }")
