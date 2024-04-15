from classes.viewer.widgets.list_widget import ListWidget
from classes.viewer.action import Action

class ActionListWidget(ListWidget):
    def __init__(self, result_widget, actions):
        super().__init__("Actions", "Run")

        self.result_widget = result_widget

        for action in actions:
            self.add_item(action.name, action)

    def on_selected(self, item):
        item.run()
        self.result_widget.clear_list()
        for result_label, result_item in item.result:
            self.result_widget.add_item(result_label, result_item)
