from PyQt6.QtWidgets import QMessageBox, QDialog
from classes.viewer.action import Action
from classes.viewer.widgets.input_dialog import InputDialog

from random import sample
from settings.db_loader import get_full_data

from classes.similarity.vector_loader import evaluate, get_vectors

from torch.nn.functional import cosine_similarity

class SimilarProblemAction(Action):
    def __init__(self):
        super().__init__("Find Similar Problems")

    def show_alert(self, text):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Alert")
        msg_box.setText(text)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        msg_box.exec()

    def run(self, main_window = None):
        dialog = InputDialog("Enter problem id.", main_window)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            problem_id = int(dialog.get_input())

        data = get_full_data()
        if not (problem_id in data["Problem"]):
            self.show_alert("No matching problem found with the id.")
            return

        problems = data["Problem"]
        problem = problems[problem_id]
        meta_id = problem.get_attribute("code").get_attribute("meta_id")
        candidates = []

        for cand in problems.values():
            cand_meta = cand.get_attribute("code")
            if cand_meta.get_attribute("meta_id") != meta_id:
                continue
            if "image" in cand_meta.get_attribute("problem_array"):
                continue
            candidates.append(cand)

        print(len(candidates))
        candidate_indices = [ cand.get_attribute("id") for cand in candidates ]
        evaluate(candidate_indices)
        vectors = get_vectors()
        get_similarity = lambda id : cosine_similarity(vectors[id], vectors[problem_id]) if vectors[id] is not None else 0
        candidate_similarities = [ (cand_id, get_similarity(cand_id)) for cand_id in candidate_indices ]

        candidate_similarities.sort(key = lambda x : -x[1])

        for cand_id, cand_sim in candidate_similarities:
            cand = problems[cand_id]
            label = "id: {0} (s={1})".format(cand_id, cand_sim)
            self.result.append((label, cand))
