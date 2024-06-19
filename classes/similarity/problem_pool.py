from settings.db_loader import get_full_data
import random

# returns all problems without image different with "problem"
def pool0 (problem):
    data = get_full_data()
    problems = data["Problem"]
    problem_code = problem.get_attribute("code")
    candidates = []
    for cand in problems.values():
        cand_code = cand.get_attribute("code")
        if cand_code == problem_code:
            continue
        if "image" in cand_code.get_attribute("problem_array"):
            continue
        candidates.append(cand)
    return candidates

# returns problem pool of size "pool_size", 
# which half of it is from same meta with original "problem",
# and another half is from different meta.
def pool1 (problem, pool_size, random_seed=0):
    all_problems = pool0(problem)

    get_meta = lambda x : x.get_attribute("code").get_attribute("meta_id")
    meta = get_meta(problem)
    same_meta = []
    diff_meta = []
    for cand in all_problems:
        if get_meta(cand) == meta:
            same_meta.append(cand)
        else:
            diff_meta.append(cand)
    
    random.seed(random_seed)
    same_size = min(len(same_meta), pool_size//2)
    diff_size = min(len(diff_meta), pool_size - same_size)

    candidates = []
    candidates.extend(random.sample(same_meta, same_size))
    candidates.extend(random.sample(diff_meta, diff_size))

    return candidates

