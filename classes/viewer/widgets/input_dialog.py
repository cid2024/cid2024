from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox

class InputDialog(QDialog):
    def __init__(self, text, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Input")

        # Setup layout
        layout = QVBoxLayout()

        # Add QLineEdit
        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText(text)
        layout.addWidget(self.line_edit)

        # Add QDialogButtonBox for OK and Cancel
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def get_input(self):
        return self.line_edit.text()
