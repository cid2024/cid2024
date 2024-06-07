from PyQt6.QtWidgets import QMessageBox, QDialog
from classes.common.data_entry import DataEntry
from classes.viewer.action import Action
from classes.viewer.widgets.input_dialog import InputDialog

from random import sample
from settings.db_loader import get_full_data

from classes.similarity.vector_loader import evaluate, get_vectors
from classes.similarity.problem_pool import pool1
from classes.similarity.util import vector_similarity

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
        placeholders = [
            "Problem id",
            "# of Problems to list"
        ]
        dialog = InputDialog(placeholders, main_window)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            input = dialog.get_input()
            problem_id = int(input[0])
            pool_size = int(input[1])
        else:
            return

        data = get_full_data()
        if not (problem_id in data["Problem"]):
            self.show_alert("No matching problem found with the id.")
            return

        problems = data["Problem"]
        problem = problems[problem_id]
        candidates = pool1(problem, pool_size)

        candidate_indices = [ cand.get_attribute("id") for cand in candidates ]
        candidate_indices.append(problem_id)
        evaluate(candidate_indices)
        
        vectors = get_vectors()
        get_similarity = lambda id : vector_similarity(vectors[id], vectors[problem_id]) if vectors[id] is not None else 0
        candidate_similarities = [ (cand_id, get_similarity(cand_id)) for cand_id in candidate_indices ]

        candidate_similarities.sort(key = lambda x : -x[1])

        get_meta = lambda x : x.get_attribute("code").get_attribute("meta_id")
        problem_meta = get_meta(problem)
        self.result = []
        for cand_id, cand_sim in candidate_similarities:
            cand = problems[cand_id]
            same_meta = (get_meta(cand) == problem_meta)
            entry = DataEntry()
            entry.set_attribute("label", "id: {} (s={:.3f})".format(cand_id, cand_sim))
            entry.set_attribute("data", cand)
            entry.set_attribute("color", "lightgreen" if same_meta else "lightcoral")
            self.result.append(entry)
