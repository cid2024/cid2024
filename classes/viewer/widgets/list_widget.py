import sys
from functools import partial
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtCore import Qt

class ListWidget(QWidget):
    def __init__(self, title_text, button_texts):
        super().__init__()

        self.label_to_item = {}

        # Initialize the QListWidget
        self.list_widget = QListWidget()

        # Set the selection mode
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

        # Create a title label
        self.title_label = QLabel(title_text)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.list_widget)

        for button_text in button_texts:
            # Create a button
            button = QPushButton(button_text)
            button.clicked.connect(partial(self.button_clicked, button_text))
            layout.addWidget(button)

        self.setLayout(layout)

    def button_clicked(self, button_text):
        # This function is triggered when the button is clicked
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            selected_item_label = selected_items[0].text()
            if selected_item_label in self.label_to_item:
                self.on_selected(button_text, self.label_to_item[selected_item_label])

    def on_selected(self, button_text, item):
        pass

    def clear_list(self):
        self.list_widget.clear()
        self.label_to_item = {}

    def add_item(self, entry):
        if not entry.has_attribute("label") or not entry.has_attribute("data"):
            return
        label = entry.get_attribute("label")
        data = entry.get_attribute("data")
        item = QListWidgetItem(label)
        self.label_to_item[label] = data

        if entry.has_attribute("color"):
            color = entry.get_attribute("color")
            item.setBackground(QBrush(QColor(color)))

        self.list_widget.addItem(item)


