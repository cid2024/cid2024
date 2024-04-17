from classes.viewer.widgets.list_widget import ListWidget
from classes.viewer.widgets.image_widget import ImageWidget
from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap
import requests

import json

def number_to_circle_string(number):
    circle_strings = " ①②③④⑤"
    if number < len(circle_strings):
        return str(circle_strings[number])
    else:
        return None

class ActionResultWidget(ListWidget):
    def __init__(self, main_window):
        super().__init__("Action Run Results", ["View Rendered", "View Raw"])
        
        self.main_window = main_window

    def on_selected(self, button_text, item):
        if not hasattr(item, "typename"):
            return
        if button_text == "View Rendered": 
            # View Rendered
            if item.typename == "Problem":
                self.main_window.clear_canvas()
                widgets = self.render_problem(item)
                for widget in widgets:
                    self.main_window.add_canvas_widget(widget)
                self.main_window.add_canvas_widget()
        else: 
            # View Raw
            self.main_window.clear_canvas()
            label = QLabel(str(item))
            label.setWordWrap(True)
            self.main_window.add_canvas_widget(label)
            self.main_window.add_canvas_widget()

    def render_array(self, array):
        widgets = []
        for piece in json.loads(array):
            typename = piece["type"]
            if (typename == "image"):
                widgets.append(ImageWidget(piece["url"]))
            else:
                label = QLabel(piece[typename])
                label.setWordWrap(True)
                widgets.append(label)
        
        return widgets

    def render_problem(self, problem):
        widgets = []

        if not problem.has_attribute("code"):
            return
        meta = problem.get_attribute("code")

        if meta.has_attribute("problem_array"):
            widgets.extend(self.render_array(meta.get_attribute("problem_array")))
            
        for i in range(1, 6):
            selection_text = "s" + str(i)
            if meta.has_attribute(selection_text):
                selection = meta.get_attribute(selection_text)
                if len(selection) > 0:
                    label = QLabel(number_to_circle_string(i) + ": " + selection)
                    label.setWordWrap(True)
                    widgets.append(label)

        if meta.has_attribute("answer_array"):
            label = QLabel("답: ")
            label.setWordWrap(True)
            widgets.append(label)
            widgets.extend(self.render_array(meta.get_attribute("answer_array")))
        
        return widgets
