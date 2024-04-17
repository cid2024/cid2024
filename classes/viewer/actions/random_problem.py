from classes.viewer.action import Action
from settings.db_loader import get_full_data
from random import sample

class RandomProblemAction(Action):
    def __init__(self):
        super().__init__("View Random Problems")

    def run(self):
        data = get_full_data()
        for id in sample(list(data["Problem"].keys()), 100):
            self.result.append(("id: " + str(id), data["Problem"][id]))
