from classes.viewer.widgets.list_widget import ListWidget
from PyQt6.QtWidgets import QWidget, QLabel, QSizePolicy

class ActionResultWidget(ListWidget):
    def __init__(self, main_window):
        super().__init__("Action run results", "View")
        
        self.main_window = main_window

    def on_selected(self, item):
        if not hasattr(item, "typename"):
            return
        if item.typename == "Problem":
            self.main_window.clear_canvas()
            label = QLabel(str(item))
            label.setWordWrap(True)
            self.main_window.add_canvas_widget(label)