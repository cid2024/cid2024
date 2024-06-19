
import json

def textify_mise(problem):
    meta = problem.get_attribute("code")

    description = ""
    problem_array = meta.get_attribute("problem_array")
    for piece in json.loads(problem_array):
        typename = piece["type"]
        if (typename == "image"):
            pass
        else:
            description += piece[typename] + "\n"
    
    selections = []
    for i in range(1, 6):
        selection_text = "s" + str(i)
        if meta.has_attribute(selection_text):
            selection = meta.get_attribute(selection_text)
            if len(selection) > 0:
                selections.append(selection)
    
    answer = json.loads(meta.get_attribute("answer_grading"))[0]

    problem_text = description + "\n"
    if len(selections) > 0:
        problem_text += "선택지:\n"
        for i in range(len(selections)):
            problem_text += str(i+1) + ": " + str(selections[i]) + "\n"
    problem_text += "\n정답: " + str(answer) + "\n"

    return problem_text

def textify_gen(problem):
    problem_text = ""
    for piece in problem.statement:
        if (piece.type == "text"):
            problem_text += piece.data + "\n"
    problem_text += "\n선택지:\n"
    
    for num, choice_array in problem.choice:
        problem_text += num + ": "
        choice_text = ""
        for piece in choice_array:
            if (len(choice_text) > 0):
                choice_text += ", "
            if (piece.type == "text"):
                choice_text += piece.data
            else:
                choice_text += "None"
        problem_text += choice_text + "\n"

    problem_text += "\n정답: " + str(problem.answer) + "\n"

    return problem_text
