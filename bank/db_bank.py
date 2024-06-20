import settings.db_loader as db_loader
from bank.models import Problem, StatementElement
from pathlib import Path
import json, pickle

def json_array_to_element_list(array):
    element_list = []
    for piece in json.loads(array):
        element = StatementElement(type=None,data=None)

        typename = piece["type"]
        if (typename == "image"):
            element.type = "image"
            element.data = piece["url"]
        else:
            # typename as "text", "math", etc. treat as text.
            element.type = "text"
            element.data = piece[typename]
        
        element_list.append(element)
    return element_list

if __name__ == "__main__":
    data = db_loader.get_full_data(False)

    problems = list(data["ProblemMeta"].values())
    converted_db = []

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
            converted = Problem(id=None,statement=None,choice=[],answer=None,explanation=None)
            converted.id = "mise." + subject + "." + str(problem.get_attribute("id"))

            converted.statement = json_array_to_element_list(problem.get_attribute("problem_array"))

            for i in range(1, 6):
                selection_text = "s" + str(i)
                if problem.has_attribute(selection_text):
                    element = StatementElement(type=None,data=None)
                    element.type = "text"
                    element.data = problem.get_attribute(selection_text)
                    converted.choice.append((str(i), [element]))
            
            converted.answer = str(json.loads(problem.get_attribute("answer_grading"))[0])
            
            converted.explanation = ""
            if problem.has_attribute("explain"):
                explanation = problem.get_attribute("explain")
                if explanation is not None and len(explanation) > 0:
                    converted.explanation = explanation
            
            converted_db.append(converted)
        except:
            pass
    
    print("Total num:", len(converted_db))
    parent_dir = Path(__file__).resolve().parent
    with open(parent_dir / "mise.pkl", "wb") as f:
        pickle.dump(converted_db, f)
                