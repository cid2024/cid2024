from classes.viewer.action import Action
from classes.common.data_entry import DataEntry
from settings.db_loader import get_full_data
from random import sample

class RandomProblemAction(Action):
    def __init__(self):
        super().__init__("View Random Problems")

    def run(self, main_window = None):
        data = get_full_data()
        for id in sample(list(data["Problem"].keys()), 100):
            entry = DataEntry()
            entry.set_attribute("label", "id: " + str(id))
            entry.set_attribute("data", data["Problem"][id])
            self.result.append(entry)
