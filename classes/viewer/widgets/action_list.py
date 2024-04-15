from classes.viewer.widgets.list_widget import ListWidget
from classes.viewer.action import Action

class ActionListWidget(ListWidget):
    def __init__(self, actions):
        super().__init__("Actions", "Run")

        for action in actions:
            self.add_item(action.name, action)

    def on_selected(self, item):
        item.run()
