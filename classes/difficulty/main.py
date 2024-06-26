import asyncio
from llm.ai_handler import AiHandler
from llm.utils import run_prompt
from settings.config_loader import get_settings
from classes.common.textify import textify_mise, textify_gen
from classes.common.data_entry import DataEntry
from bank.models import Problem
import re

import os
import pickle

difficulties = None


def get_difficulties():
    global difficulties
    if difficulties is not None:
        return difficulties
    
    file_path = os.path.join(os.path.dirname(__file__), "difficulties.pkl.usage")

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        file = open(file_path, "rb")
        difficulties = pickle.load(file)
        file.close()

    if difficulties is None:
        difficulties = {}
    
    return difficulties


def evaluate(problem, overwrite: bool = False):
    get_difficulties()
    global difficulties
    if overwrite or problem.id not in difficulties:
        difficulties[problem.id] = difficulty(textify_gen(problem))

    file_path = os.path.join(os.path.dirname(__file__), "difficulties.pkl.usage")
    file = open(file_path, "wb")
    pickle.dump(difficulties, file)
    file.close()


def difficulty(problem_text: str) -> int:
    handler = AiHandler()
    prompt = get_settings()["difficulty_eval"]
    result = asyncio.run(
        run_prompt(
            handler,
            prompt,
            user_vars={
                "problem": problem_text
            },
            system_vars=dict(),
        )
    )

    pattern = r"%%%(\d+)%%%"
    match = re.search(pattern, result)

    if match:
        return int(match.group(1))
    else:
        return 0


def difficulty_mise(problem: DataEntry) -> int:
    return difficulty(textify_mise(problem))


def difficulty_gen(problem: Problem) -> int:
    evaluate(problem)
    return difficulties[problem.id]
