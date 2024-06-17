import asyncio
import pprint
from dataclasses import dataclass

from llm.ai_handler import AiHandler
from llm.utils import run_prompt
from settings.config_loader import get_settings
from settings.textbook_loader import get_textbook
from util.parse import parse_llm_yaml


@dataclass(kw_only=True)
class HistoricEvent:
    name: str
    explanation: str


def extract_historic_events(
        handler: AiHandler,
        reference: str,
) -> list[HistoricEvent]:
    prompt = get_settings()["event_extract_historic_events_prompt"]
    response = asyncio.run(
        run_prompt(
            handler,
            prompt,
            user_vars={
                "reference": reference,
            },
            system_vars=dict(),
        )
    ).strip()

    try:
        data = parse_llm_yaml(response)["historic_event"]

        ret: list[HistoricEvent] = []
        for item in data:
            name = item.get("event_name", "").strip()
            explanation = item.get("explanation", "").strip()

            if name and explanation:
                ret.append(HistoricEvent(
                    name=name,
                    explanation=explanation,
                ))

        return ret
    except:
        return []


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    textbook_name = "korean"
    textbook = list(map(str, filter(None, get_textbook(textbook_name))))
    page = 74
    reference = '\n'.join(textbook[page: page+7])

    handler = AiHandler()

    events = extract_historic_events(handler, reference)
    pp.pprint(events)
