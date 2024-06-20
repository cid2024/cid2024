from bank.models import Problem
from bank.loader import get_problems_dict

from classes.difficulty.main import difficulty_gen
from classes.similarity.main import similarity_gen

import random


def get_user_skill(history):
    user_skill = 0
    for problem, correct in history:
        dif = difficulty_gen(problem)
        if correct:
            user_skill = min(max(user_skill, dif) + 1, 10)
        else:
            user_skill = max(min(user_skill, dif) - 1, 0)
    return user_skill


# Get recommended problem.
# It will pick problem in problem_pool. If it is None, problem will be picked in all problems. 
def recommend_problem(
        history_data: list[tuple[str, bool]],
        problem_pool: list[Problem] | None = None,
) -> Problem:
    full_problems_dict = get_problems_dict()

    if problem_pool is None:
        problem_pool = list(full_problems_dict.values())

    if not history_data:
        return random.choice(problem_pool)

    history = [
        (
            full_problems_dict[pid],
            correct,
        )
        for pid, correct in history_data
        if pid in full_problems_dict
    ]

    user_skill = get_user_skill(history)

    tried_pid = set([record[0].id for record in history])

    # Filter problems already in history
    problem_pool = [
        problem
        for problem in problem_pool
        if problem.id not in tried_pid
    ]

    # Try to filter problems by user skill
    user_skill_pool = [
        problem
        for problem in problem_pool
        if abs(difficulty_gen(problem) - user_skill) <= 1
    ]

    if len(user_skill_pool) > 0:
        problem_pool = user_skill_pool

    (last_problem, last_problem_correct) = history[-1]

    if last_problem_correct:
        if problem_pool:
            return random.choice(problem_pool)
        else:
            return random.choice(list(full_problems_dict.values()))
    else:
        max_similarity = -1
        argmax = None
        for problem in problem_pool:
            similarity = similarity_gen(problem, last_problem)
            if similarity > max_similarity:
                max_similarity = similarity
                argmax = problem
        # print("Similarity: ", max_similarity)

        if argmax is None:
            return random.choice(list(full_problems_dict.values()))

        return argmax


if __name__ == "__main__":
    print(recommend_problem(history_data=[('gen.region.map.512', True)]).id)
