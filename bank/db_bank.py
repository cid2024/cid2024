import json, pickle
import pprint
import re

from bank import models
from pathlib import Path

import settings.db_loader as db_loader


def json_array_to_element_list(json_str: str) -> list[models.StatementElement]:
    try:
        data = json.loads(json_str)
    except:
        return []

    if not isinstance(data, list):
        return []

    ret: list[models.StatementElement] = []
    for item in data:
        if not isinstance(item, dict):
            continue

        typename = item.get("type", "")

        if typename == "image":
            url = item.get("url", "")
            if url:
                ret.append(
                    models.StatementElement(
                        type="image",
                        data=url,
                    )
                )
        elif typename in ["text", "math"]:
            text = item.get(typename, "")

            clean = re.compile('<.*?>')
            text = re.sub(clean, '', text)
            text = '\n'.join(map(str.strip, text.split('\n'))).strip()

            if text:
                ret.append(
                    models.StatementElement(
                        type="text",
                        data=text,
                    )
                )

    return ret


def commit_db() -> None:
    data = db_loader.get_full_data(False)

    problems = list(data["ProblemMeta"].values())
    converted_db: list[models.Problem] = []

    for problem in problems:
        try:
            subject = problem.get_attribute("meta_id").get_attribute("subject")
            if subject == "한국사":
                subject = "korean"
            elif subject == "동아시아사":
                subject = "eastasia"
            elif subject == "세계사":
                subject = "world"
            else:
                continue

            problem_id = f"mise.{subject}.{problem.get_attribute('id')}"
            problem_statement = json_array_to_element_list(problem.get_attribute("problem_array"))
            if not problem_statement:
                continue

            problem_choices: list[list[models.StatementElement]] = []

            for i in range(1, 6):
                selection_text = "s" + str(i)
                if problem.has_attribute(selection_text):
                    text = str(problem.get_attribute(selection_text)).strip()
                    if not text:
                        continue

                    clean = re.compile('<.*?>')
                    text = re.sub(clean, '', text)
                    text = '\n'.join(map(str.strip, text.split('\n'))).strip()
                    if not text:
                        continue

                    problem_choices.append(
                        [
                            models.StatementElement(
                                type="text",
                                data=text,
                            ),
                        ]
                    )

            problem_answer = '\n'.join([
                item.data
                for item in json_array_to_element_list(problem.get_attribute("answer_array"))
                if item.type == "text"
            ])

            problem_explanation = '\n'.join([
                item.data
                for item in json_array_to_element_list(problem.get_attribute("explain_array"))
                if item.type == "text"
            ])

            converted_db.append(
                models.Problem(
                    id=problem_id,
                    statement=problem_statement,
                    choice=[
                        (
                            ["①", "②", "③", "④", "⑤"][idx],
                            choice,
                        )
                        for idx, choice in enumerate(problem_choices)
                    ],
                    answer=problem_answer,
                    explanation=problem_explanation,
                )
            )
        except:
            pass

    with open("mise.pkl", "wb") as f:
        pickle.dump(converted_db, f)


mise_problems: list[models.Problem] = []


def load_db() -> None:
    global mise_problems

    parent_path = Path(__file__).parent
    with open(parent_path / "mise.pkl.final", "rb") as f:
        mise_problems = pickle.load(f)


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    load_db()

    pp.pprint(mise_problems)
