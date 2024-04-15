from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QScrollArea

from classes.viewer.widgets.action_list import ActionListWidget
from classes.viewer.widgets.action_result import ActionResultWidget
from classes.viewer.actions.all_problem import AllProblemAction

from settings.db_loader import get_full_data

class ViewerMainWindow(QMainWindow):
    def __init__(self, actions):
        super().__init__()

        self.canvas_scroll_area = QScrollArea(self)
        self.canvas_scroll_area.setWidgetResizable(True)
        
        self.canvas = QWidget()
        self.canvas_layout = QVBoxLayout(self.canvas)
        self.canvas_scroll_area.setWidget(self.canvas)

        self.action_result = ActionResultWidget(self)
        self.action_list = ActionListWidget(self.action_result, actions)

        # Main widget that holds the layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main horizontal layout
        self.layout = QHBoxLayout(self.central_widget)

        # First widget (flexible)
        self.layout.addWidget(self.canvas_scroll_area)  # Add left widget to the main layout

        # Vertical line between left and middle
        self.line1 = QFrame()
        self.line1.setFrameShape(QFrame.Shape.VLine)
        self.line1.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(self.line1)

        # Second widget (fixed size)
        self.action_list.setFixedWidth(200)  # Fixed width
        self.layout.addWidget(self.action_list)  # Add middle widget to the main layout

        # Vertical line between middle and right
        self.line2 = QFrame()
        self.line2.setFrameShape(QFrame.Shape.VLine)
        self.line2.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(self.line2)

        # Third widget (fixed size)
        self.action_result.setFixedWidth(200)  # Fixed width
        self.layout.addWidget(self.action_result)  # Add right widget to the main layout

        # Window settings
        self.setWindowTitle("Viewer")
        self.resize(1000, 600)

    def clear_canvas(self):
        for i in reversed(range(self.canvas_layout.count())): 
            widget = self.canvas_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
    
    def add_canvas_widget(self, widget):
        self.canvas_layout.addWidget(widget)

if __name__ == "__main__":
    print("# Viewer will be opened after preprocessing db.")
    get_full_data()

    app = QApplication([])
    window = ViewerMainWindow(actions=[ AllProblemAction() ])
    window.show()
    app.exec()
