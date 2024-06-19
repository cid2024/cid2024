import pickle
import pprint
import random
from pathlib import Path

import gen.distractor.db.main as distractor_db
from bank import models
from gen.distractor.db.main import ReferenceRecord


def make_choose_all_problems_from_records(
        records: list[ReferenceRecord],
        id_prefix: str,
) -> list[models.Problem]:
    problems: list[models.Problem] = []

    records = [record for record in records if record.improved_distractors]

    cnt = 0

    while 3 <= len(records):
        n = random.randint(3, min(4, len(records)))

        indices = [
            [
                idx
                for idx, score in enumerate(records[i].improved_distractor_scores)
                if 9 <= score.accuracy_score and 8 <= score.sense_score
            ]
            for i in range(n)
        ]

        invert: bool = random.choice([True, False])
        answer_bit: int = 0

        can_be_wrong: int = 0
        for i in range(n):
            if indices[i]:
                can_be_wrong |= 1 << i

        true_sels = [
            key
            for key in range(1, 1 << n)
            if ((((1 << n) - 1) ^ key) | can_be_wrong) == can_be_wrong
        ]

        false_sels = [
            key
            for key in range(1, 1 << n)
            if (key | can_be_wrong) == can_be_wrong
        ]

        invert: bool = random.choice([True, False])

        if invert and not false_sels:
            invert = False

        answer_bit = random.choice(true_sels if not invert else false_sels)

        cnt += 1
        problems.append(models.Problem(
            id=f"{id_prefix}.choose_all.{cnt}",
            statement=[
                models.StatementElement(
                    type="text",
                    data=(
                        f"다음 중 "
                        f"{'옳은' if not invert else '옳지 않은'} 것을 모두 고르세요."
                    ),
                ),
            ],
            choice=[
                (
                    ["가", "나", "다", "라", "마"][i],
                    [
                        models.StatementElement(
                            type="text",
                            data=(
                                records[i].key_sentence.sentence
                                if (bool(answer_bit & (1 << i)) is bool(not invert))
                                else records[i].improved_distractors[random.choice(indices[i])].improved_distractor
                            ),
                        ),
                    ],
                )
                for i in range(n)
            ],
            answer=", ".join([
                ["가", "나", "다", "라", "마"][i]
                for i in range(n)
                if (answer_bit & (1 << i))
            ]),
            explanation="\n".join([
                records[i].key_sentence.sentence
                for i in range(n)
                if (bool(answer_bit & (1 << i)) is bool(invert))
            ]),
        ))

        records = records[n:]

    return problems


def make_choose_all_problems_by_page(
        records: list[ReferenceRecord],
        id_prefix: str,
) -> list[models.Problem]:
    problems: list[models.Problem] = []

    data: dict[int, list[ReferenceRecord]] = {}

    for record in records:
        data.setdefault(record.page, []).append(record)

    for page, records in data.items():
        problems.extend(
            make_choose_all_problems_from_records(
                records,
                f"{id_prefix}.page.{page}",
            )
        )

    return problems


def make_choose_all_problems() -> list[models.Problem]:
    problems: list[models.Problem] = []

    problems.extend(
        make_choose_all_problems_by_page(
            distractor_db.world_records,
            "gen.choose_all.distractor.world",
        )
    )

    problems.extend(
        make_choose_all_problems_by_page(
            distractor_db.korean_records,
            "gen.choose_all.distractor.korean",
        )
    )

    problems.extend(
        make_choose_all_problems_by_page(
            distractor_db.eastasia_records,
            "gen.choose_all.distractor.eastasia",
        )
    )

    return problems


def commit_db():
    distractor_db.load_db()
    problems = make_choose_all_problems()

    with open("choose_all_problems.pkl", "wb") as f:
        pickle.dump(problems, f)


choose_all_problems: list[models.Problem] = []


def load_db() -> None:
    global choose_all_problems

    parent_dir = Path(__file__).resolve().parent
    with open(parent_dir / "choose_all_problems.pkl.final", "rb") as f:
        choose_all_problems = pickle.load(f)


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    load_db()

    pp.pprint(choose_all_problems)
