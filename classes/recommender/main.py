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
            user_skill = max(user_skill, dif) + 1
        else:
            user_skill = min(user_skill, dif) - 1
    return user_skill

# Get recommended problem.
# It will pick problem in problem_pool. If it is None, problem will be picked in all problems. 
def recommend_problem (history:list[tuple[Problem, bool]], problem_pool:list[Problem] = None) -> Problem:
    user_skill = get_user_skill(history)

    tried_pid = set([record[0].id for record in history])

    if problem_pool == None:
        all_problems = list(get_problems_dict.values())
        problem_pool = [ problem for problem in all_problems if problem.id not in tried_pid ]

    problem_pool = [ problem for problem in problem_pool if abs(difficulty_gen(problem) - user_skill) <= 2 ]

    user_skill = get_user_skill(history)

    (last_problem, last_problem_correct) = history[-1]

    if last_problem_correct:
        return random.choice(problem_pool)
    else:
        max_similarity = -1
        argmax = None
        for problem in problem_pool:
            similarity = similarity_gen(problem, last_problem)
            if similarity > max_similarity:
                max_similarity = similarity
                argmax = problem
        # print("Similarity: ", max_similarity)
        return argmax

