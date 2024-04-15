from classes.viewer.action import Action

class AllProblemAction(Action):
    def __init__(self):
        super().__init__("View All Problems")

    def run(self):
        print("Test")