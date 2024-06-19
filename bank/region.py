import asyncio
import pickle
import pprint
from dataclasses import dataclass
from pathlib import Path

import gen.event.db.main as event_db
import gen.region.db.main as region_db

from bank import models
from gen.distractor.db.main import ReferenceRecord
from llm.ai_handler import AiHandler
from llm.utils import run_prompt
from settings.config_loader import get_settings
from util.parse import parse_llm_yaml


def make_region_blank_problems() -> list[models.Problem]:
    events = (
        event_db.eastasia_historic_events
        + event_db.korean_historic_events
        + event_db.world_historic_events
    )

    problems: list[models.Problem] = []

    for region_idx, region_name in enumerate(region_db.region_names):
        region_events = [
            event for event in events
            if region_name in (event.name + " " + event.explanation)
        ]

        problems.extend([
            models.Problem(
                id=f"gen.region.blank.{region_idx}.{idx}",
                statement=[
                    models.StatementElement(
                        type="text",
                        data=(
                            "다음 설명 중 빈칸에 " +
                            ("공통적으로 " if 1 < event.explanation.count(region_name) else "") +
                            "들어갈 지명을 적으세요."
                        ),
                    ),
                    models.StatementElement(
                        type="text",
                        data=event.explanation.replace(region_name, "(___)"),
                    ),
                ],
                choice=[],
                answer=region_name,
                explanation='',
            )
            for idx, event in enumerate(region_events)
        ])

    return problems


@dataclass(kw_only=True)
class RegionBlankDistractor:
    name: str
    en_name: str


def gen_region_blank_distractors(
        handler: AiHandler,
        problems: list[models.Problem],
) -> list[tuple[models.Problem, list[RegionBlankDistractor]]]:
    ret: list[tuple[models.Problem, list[RegionBlankDistractor]]] = []

    prompt = get_settings()["bank_region_distractors_prompt"]

    for idx, problem in enumerate(problems):
        print("@" * 10, idx, '/', len(problems))

        response = asyncio.run(
            run_prompt(
                handler,
                prompt,
                user_vars={
                    "statement": '\n'.join(map(lambda x: x.data, problem.statement)),
                },
                system_vars=dict(),
            )
        )

        try:
            data = parse_llm_yaml(response)["place"]
            distractors: list[RegionBlankDistractor] = []

            if isinstance(data, list):
                for item in data:
                    kor_name = item.get("kor_name", "").strip()
                    eng_name = item.get("eng_name", "").strip()

                    if kor_name and eng_name:
                        distractors.append(
                            RegionBlankDistractor(
                                name=kor_name,
                                en_name=eng_name,
                            )
                        )

            if distractors:
                ret.append((problem, distractors))
        except:
            pass

    return ret


def commit_db_distractors() -> None:
    problems = make_region_blank_problems()

    handler = AiHandler()
    ret = gen_region_blank_distractors(handler, problems)

    # Save ret as pickle.
    with open("region_blank_distractors.pickle", "wb") as f:
        pickle.dump(ret, f)


region_blank_distractors: list[tuple[models.Problem, list[RegionBlankDistractor]]] = []


def load_db_distractors() -> None:
    global region_blank_distractors

    parent_dir = Path(__file__).resolve().parent
    with open(parent_dir / "region_blank_distractors.pickle.final", "rb") as f:
        region_blank_distractors = pickle.load(f)


@dataclass(kw_only=True)
class RegionBlankPossibleAnswer:
    name: str
    en_name: str
    explanation: str


@dataclass(kw_only=True)
class RegionBlankRecord:
    problem: models.Problem
    distractors: list[RegionBlankDistractor]
    possible_answers: list[RegionBlankPossibleAnswer]


def commit_db_possible_records() -> None:
    handler = AiHandler()
    prompt = get_settings()["bank_region_multiple_answer_check_prompt"]

    region_blank_records: list[RegionBlankRecord] = []

    for idx, (problem, distractors) in enumerate(region_blank_distractors):
        print("@" * 10, idx, '/', len(region_blank_distractors))

        region_name = problem.answer
        possible_answers: list[RegionBlankPossibleAnswer] = []

        response = asyncio.run(
            run_prompt(
                handler,
                prompt,
                user_vars={
                    "statement": '\n'.join(map(lambda x: x.data, problem.statement)),
                    "answer": region_name,
                },
                system_vars=dict(),
            )
        )

        try:
            data = parse_llm_yaml(response)["answer"]
            if isinstance(data, list):
                for item in data:
                    kor_name = item.get("kor_name", "").strip()
                    eng_name = item.get("eng_name", "").strip()
                    explanation = item.get("explanation", "").strip()

                    if kor_name and eng_name and explanation:
                        possible_answers.append(
                            RegionBlankPossibleAnswer(
                                name=kor_name,
                                en_name=eng_name,
                                explanation=explanation,
                            )
                        )
        except:
            pass

        region_blank_records.append(
            RegionBlankRecord(
                problem=problem,
                distractors=distractors,
                possible_answers=possible_answers,
            )
        )

    # Save ret as pickle.
    with open("region_blank_possible_records.pickle", "wb") as f:
        pickle.dump(region_blank_records, f)


region_blank_records: list[RegionBlankRecord] = []


def load_db_possible_records() -> None:
    global region_blank_records

    parent_dir = Path(__file__).resolve().parent
    with open(parent_dir / "region_blank_possible_records.pickle.final", "rb") as f:
        region_blank_records = pickle.load(f)


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4, width=120)

    event_db.load_db()
    region_db.load_db()

    load_db_possible_records()

    good_records = [
        record for record in region_blank_records
        if len(record.possible_answers) <= 2
    ]

    for record in good_records:
        pp.pprint(record)
