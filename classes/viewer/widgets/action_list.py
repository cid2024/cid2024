from classes.viewer.widgets.list_widget import ListWidget
from classes.viewer.action import Action

class ActionListWidget(ListWidget):
    def __init__(self, main_window, actions):
        super().__init__("Actions", ["Run"])

        self.main_window = main_window
        self.result_widget = main_window.action_result

        for action in actions:
            self.add_item(action.name, action)

    def on_selected(self, button_text, item):
        item.run(self.main_window)
        self.result_widget.clear_list()
        for result_label, result_item in item.result:
            self.result_widget.add_item(result_label, result_item)
