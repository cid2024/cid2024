import pickle
import pprint
from pathlib import Path

from gen.event.extract import extract_historic_events, HistoricEvent
from llm.ai_handler import AiHandler
from settings.textbook_loader import get_textbook


eastasia_historic_events: list[HistoricEvent] = []
korean_historic_events: list[HistoricEvent] = []
world_historic_events: list[HistoricEvent] = []


def load_db():
    global eastasia_historic_events, korean_historic_events, world_historic_events

    parent_dir = Path(__file__).resolve().parent

    with open(parent_dir / "historic_events__eastasia.pkl.final", 'rb') as f:
        eastasia_historic_events = pickle.load(f)

    with open(parent_dir / "historic_events__korean.pkl.final", 'rb') as f:
        korean_historic_events = pickle.load(f)

    with open(parent_dir / "historic_events__world.pkl.final", 'rb') as f:
        world_historic_events = pickle.load(f)


def commit_db():
    handler = AiHandler()

    for textbook_name in [
        "eastasia",
        "korean",
        "world",
    ]:
        textbook = list(map(str, filter(None, get_textbook(textbook_name))))
        n_pages = len(textbook)
        if n_pages < 7:
            continue

        events: list[HistoricEvent] = []

        run_cnt = 0

        for page in range(0, n_pages - 6, 6):
            reference = '\n'.join(textbook[page: page+7])
            events.extend(extract_historic_events(handler, reference))

            run_cnt += 1
            if run_cnt % 4 == 0:
                file_path = f"historic_events__{textbook_name}.{run_cnt}.pkl"
                with open(file_path, 'wb') as f:
                    pickle.dump(events, f)

            print("@" * 10 + f" End {page}/{n_pages} of {textbook_name}")

        file_path = f"historic_events__{textbook_name}.pkl"
        with open(file_path, 'wb') as f:
            pickle.dump(events, f)


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    # commit_db()

    load_db()

    pp.pprint(eastasia_historic_events)
