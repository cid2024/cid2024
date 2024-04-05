import logging
import openai
from aiolimiter import AsyncLimiter
from openai import OpenAI, AzureOpenAI
from retry import retry

from settings.config_loader import get_settings
from log import get_logger

logger = get_logger(__name__)
OPENAI_RETRIES = 5


class AiHandler:
    """
    This class handles interactions with the OpenAI API for chat completions.
    It initializes the API key and other settings from a configuration file,
    and provides a method for performing chat completions using the OpenAI ChatCompletion API.
    """

    def __init__(self):
        """
        Initializes the OpenAI API key and other settings from a configuration file.
        Raises a ValueError if the OpenAI key is missing.
        """
        self.limiter = AsyncLimiter(get_settings().config.max_requests_per_minute)
        try:
            self.client = AzureOpenAI(
                azure_endpoint=get_settings().azure.endpoint,
                api_key=get_settings().azure.key,
                api_version=get_settings().azure.version,
            )

            self.azure = True
        except AttributeError as e:
            raise ValueError("OpenAI key is required") from e

    @retry(
        exceptions=AttributeError,
        tries=OPENAI_RETRIES,
        delay=2,
        backoff=2,
        jitter=(1, 3),
    )
    async def chat_completion(
            self,
            system: str,
            user: str,
            temperature: float = 0.2,
            frequency_penalty: float = 0.1,
    ):
        model = get_settings().config.model

        try:
            if get_settings().config.verbosity_level >= 2:
                logging.debug(
                    f"Generating completion with {model}"
                )

            async with self.limiter:
                logger.info("-----------------")
                logger.info("Running inference ...")
                logger.debug(f"system:\n{system}")
                logger.debug(f"user:\n{user}")

                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    temperature=temperature,
                    frequency_penalty=frequency_penalty,
                    timeout=get_settings().config.ai_timeout,
                    max_tokens=get_settings().config.max_tokens,
                )
        except Exception as e:
            logging.error("Unknown error during OpenAI inference: ", e)
            raise e
        if response is None or len(response.choices) == 0:
            raise Exception("No response from OpenAI")
        resp = response.choices[0].message.content
        finish_reason = response.choices[0].finish_reason
        logger.debug(f"response:\n{resp}")
        logger.info('done')
        logger.info("-----------------")
        return resp, finish_reason
