from classes.viewer.widgets.list_widget import ListWidget
from classes.common.data_entry import DataEntry

class ActionListWidget(ListWidget):
    def __init__(self, main_window, actions):
        super().__init__("Actions", ["Run"])

        self.main_window = main_window
        self.result_widget = main_window.action_result

        for action in actions:
            entry = DataEntry()
            entry.set_attribute("label", action.name)
            entry.set_attribute("data", action)
            self.add_item(entry)

    def on_selected(self, button_text, item):
        item.run(self.main_window)
        self.result_widget.clear_list()
        for result in item.result:
            self.result_widget.add_item(result)
