from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox

class InputDialog(QDialog):
    def __init__(self, texts, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Input")

        # Setup layout
        layout = QVBoxLayout()

        # Add QLineEdit
        self.line_edits = []
        
        for text in texts:
            line_edit = QLineEdit(self)
            line_edit.setPlaceholderText(text)
            self.line_edits.append(line_edit)
            layout.addWidget(line_edit)

        # Add QDialogButtonBox for OK and Cancel
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def get_input(self):
        input = []
        for line_edit in self.line_edits:
            input.append(line_edit.text())
        return input
