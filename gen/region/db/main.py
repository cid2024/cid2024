import asyncio
import pprint
from pathlib import Path

import gen.event.db.main as event_db
from llm.ai_handler import AiHandler
from llm.utils import run_prompt
from settings.config_loader import get_settings


region_names: list[str] = []


def load_db() -> None:
    global region_names

    parent_dir = Path(__file__).resolve().parent
    with open(parent_dir / "names.txt", "r") as f:
        region_names = f.read().split("\n")

    region_names = sorted(list(set(filter(None, map(str, region_names)))))


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

    load_db()

    pp.pprint(region_names)

    event_db.load_db()

    events = (
        event_db.eastasia_historic_events
        + event_db.korean_historic_events
        + event_db.world_historic_events
    )

    keyword = region_names[15]

    for event in events:
        if keyword in (event.name + " " + event.explanation):
            pp.pprint(event)
