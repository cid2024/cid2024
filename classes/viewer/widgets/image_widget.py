import sys
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QSize, Qt
import requests
from io import BytesIO

class ImageWidget(QLabel):
    def __init__(self, url):
        super().__init__()
        self.init_ui(url)
    
    def load_image_from_url(self, url):
        response = requests.get(url)
        image_bytes = BytesIO(response.content)
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(image_bytes.getvalue())
        return self.pixmap

    def init_ui(self, url):
        self.setPixmap(self.load_image_from_url(url))
        self.original_pixmap = self.pixmap
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(1, 1)

    def setPixmap(self, pixmap):
        super().setPixmap(pixmap)
        self.updateGeometry()  # Update the geometry to trigger sizeHint update
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.original_pixmap:
            # Scale pixmap to fit label width while maintaining aspect ratio
            scaled_pixmap = self.original_pixmap.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio)
            super().setPixmap(scaled_pixmap)

    def sizeHint(self):
        # Calculate size hint based on the width of the container and the aspect ratio of the pixmap
        width = min(self.parentWidget().width() if self.parentWidget() else self.width(), self.original_pixmap.width())
        height = int(width * (self.original_pixmap.height() / self.original_pixmap.width()))
        return QSize(width, height)

