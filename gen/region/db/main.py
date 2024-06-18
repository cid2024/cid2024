import asyncio
import pprint

import gen.event.db.main as event_db
from llm.ai_handler import AiHandler
from llm.utils import run_prompt
from settings.config_loader import get_settings


def prev_gather():
    pp = pprint.PrettyPrinter(indent=4)

    event_db.load_db()
    events = event_db.world_historic_events

    data: list[str] = []

    for s in range(0, len(events), 5):
        reference = "\n\n".join([
            f"# {historic_event.name}\n"
            f"{historic_event.explanation}"
            for historic_event in events[s: min(len(events), s + 5)]
        ])

        handler = AiHandler()

        prompt = get_settings()["region_extract_regions_from_events_prompt"]
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

        data.extend(list(response.split('\n')))

    print("@" * 50)
    for d in data:
        print(d)


def prev_text():
    pp = pprint.PrettyPrinter(indent=4)

    with open("names.txt", "r") as f:
        names = f.read().split("\n")

    names = list(set(names))

    for name in names:
        print(name)

    print()
    print(len(names))


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    event_db.load_db()

    events = (
        event_db.eastasia_historic_events
        + event_db.korean_historic_events
        + event_db.world_historic_events
    )

    keyword = "시마네현"

    for event in events:
        if keyword in (event.name + " " + event.explanation):
            pp.pprint(event)
