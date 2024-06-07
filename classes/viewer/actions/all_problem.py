from classes.viewer.action import Action
from classes.common.data_entry import DataEntry
from settings.db_loader import get_full_data

class AllProblemAction(Action):
    def __init__(self):
        super().__init__("View All Problems")

    def run(self, main_window = None):
        data = get_full_data()
        for id, problem in data["Problem"].items():
            entry = DataEntry()
            entry.set_attribute("label", "id: " + str(id))
            entry.set_attribute("data", problem)
            self.result.append(entry)
