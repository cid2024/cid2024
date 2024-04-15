from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame

from classes.viewer.widgets.action_list import ActionListWidget
from classes.viewer.widgets.action_result import ActionResultWidget
from classes.viewer.actions.all_problem import AllProblemAction

class ViewerMainWindow(QMainWindow):
    def __init__(self, actions):
        super().__init__()

        # Main widget that holds the layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main horizontal layout
        self.layout = QHBoxLayout(self.central_widget)

        # First widget (flexible)
        self.left_widget = QWidget()  # Left widget
        self.left_layout = QVBoxLayout(self.left_widget)
        self.layout.addWidget(self.left_widget)  # Add left widget to the main layout

        # Vertical line between left and middle
        self.line1 = QFrame()
        self.line1.setFrameShape(QFrame.Shape.VLine)
        self.line1.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(self.line1)

        # Second widget (fixed size)
        self.middle_widget = ActionListWidget(actions)  # Middle widget
        self.middle_widget.setFixedWidth(200)  # Fixed width
        self.layout.addWidget(self.middle_widget)  # Add middle widget to the main layout

        # Vertical line between middle and right
        self.line2 = QFrame()
        self.line2.setFrameShape(QFrame.Shape.VLine)
        self.line2.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(self.line2)

        # Third widget (fixed size)
        self.right_widget = ActionResultWidget()  # Right widget
        self.right_widget.setFixedWidth(200)  # Fixed width
        self.layout.addWidget(self.right_widget)  # Add right widget to the main layout

        # Window settings
        self.setWindowTitle("Viewer")
        self.resize(1000, 600)

if __name__ == "__main__":
    app = QApplication([])
    window = ViewerMainWindow(actions=[ AllProblemAction() ])
    window.show()
    app.exec()
