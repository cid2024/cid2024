import pickle
import pprint
from pathlib import Path

import gen.distractor.db.main as distractor_db
from bank import models
from gen.distractor.db.main import ReferenceRecord


def make_tf_problems_from_record(
        record: ReferenceRecord,
        id_prefix: str,
) -> list[models.Problem]:
    problems: list[models.Problem] = []

    intro_statement = models.StatementElement(
        type="text",
        data=(
            f"다음은 {record.key_sentence.keyword}에 대한 설명입니다. "
            f"옳으면 T, 그렇지 않으면 F를 입력하세요."
        )
    )

    problems.append(models.Problem(
        id=f"{id_prefix}.true",
        statement=[
            intro_statement,
            models.StatementElement(
                type="text",
                data=record.key_sentence.sentence,
            ),
        ],
        choice=[],
        answer="T",
        explanation="",
    ))

    for idx, score in enumerate(record.improved_distractor_scores):
        if score.accuracy_score < 9 or score.sense_score < 8:
            continue

        problems.append(models.Problem(
            id=f"{id_prefix}.false.{idx}",
            statement=[
                intro_statement,
                models.StatementElement(
                    type="text",
                    data=record.improved_distractors[idx].improved_distractor,
                ),
            ],
            choice=[],
            answer="F",
            explanation=record.key_sentence.sentence,
        ))

    return problems


def make_tf_problems() -> list[models.Problem]:
    problems: list[models.Problem] = []

    for idx, record in enumerate(distractor_db.world_records):
        problems.extend(
            make_tf_problems_from_record(
                record,
                f"gen.tf.distractor.world.{idx}",
            )
        )

    for idx, record in enumerate(distractor_db.korean_records):
        problems.extend(
            make_tf_problems_from_record(
                record,
                f"gen.tf.distractor.korean.{idx}",
            )
        )

    for idx, record in enumerate(distractor_db.eastasia_records):
        problems.extend(
            make_tf_problems_from_record(
                record,
                f"gen.tf.distractor.eastasia.{idx}",
            )
        )

    return problems


def commit_db():
    distractor_db.load_db()
    problems = make_tf_problems()

    with open("tf_problems.pkl", "wb") as f:
        pickle.dump(problems, f)


tf_problems: list[models.Problem] = []


def load_db():
    global tf_problems

    with open("tf_problems.pkl.final", "rb") as f:
        tf_problems = pickle.load(f)


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    load_db()

    pp.pprint(tf_problems)
