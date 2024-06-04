from classes.viewer.action import Action
from settings.db_loader import get_full_data

class AllProblemAction(Action):
    def __init__(self):
        super().__init__("View All Problems")

    def run(self, main_window = None):
        data = get_full_data()
        for id, problem in data["Problem"].items():
            self.result.append(("id: " + str(id), problem))
